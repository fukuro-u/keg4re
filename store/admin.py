from django.contrib import admin
# from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Product, Customer,  Order, OrderItem, Coupon


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = self.get_category_queryset()
        return form

    def get_category_queryset(self):
        """
        Sorted
        """
        categories = Category.objects.all()
        return self.get_sorted_categories(categories)

    def get_sorted_categories(self, categories, parent=None, level=0):
        """
        Get sorted
        """
        sorted_categories = []
        children = categories.filter(parent=parent).order_by('name')
        for child in children:
            sorted_categories.append((child.pk, '---' * level + child.name))
            sorted_categories.extend(self.get_sorted_categories(categories, child, level + 1))
        return sorted_categories

    def clean(self, obj):
        if obj.parent and obj.parent == obj:
             raise ValidationError("A category cannot be its own parent")

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'customer', 'address', 'phone', 'date', 'status', 'total', 'coupon')
    readonly_fields = ('total',)
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_total()

class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'discount_type', 'discount')
    list_filter = ('discount_type',)
    search_fields = ('name', 'code')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)