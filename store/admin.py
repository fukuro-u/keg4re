from django.contrib import admin
from django import forms
import json
from django.utils.safestring import mark_safe
from django.forms import ChoiceField, Widget, Select
from django.core.exceptions import ValidationError
from .models import Category, Product, Customer,  Order, OrderItem, Coupon
from django.urls import reverse
from django.conf import settings
import os
from django.utils.html import format_html

# from django_json_editor import JSONEditorWidget


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
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
            sorted_categories.append((child.pk,  '---' * level + child.name))
            sorted_categories.extend(self.get_sorted_categories(categories, child, level + 1))
        return sorted_categories

    def clean(self, obj):
        if obj.parent and obj.parent == obj:
             raise ValidationError("A category cannot be its own parent")

class JSONAttributeWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'cols': 80, 'rows': 10})

    def render(self, name, value, attrs=None, renderer=None):
        if not value:
            value = '{}'
        return format_html('<textarea name="{}" cols="{}" rows="{}">{}</textarea>', name, self.attrs.get('cols', 80), self.attrs.get('rows', 10), json.dumps(value, indent=4))

    def value_from_form(self, data, name):
        json_data = data.get(name, '{}')
        return json.loads(json_data)

class ImageSelectWidget(forms.Select):
    name = "cascicndimemm"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.choices = self.get_image_choices()
        print(self.name)
        self.name = "cascicndimemm"
        self.choices = [
            { 
                "label" : "cai ccc",
                "value" : "/media/uploads/products/laptop-gaming-msi-bravo-15-b7ed_c36cc4b4ad574b2382b658cce8fa5e0b_grande.webp"
            },
        ]
        self.template_name = 'admin/widgets/image_select.html'

    def get_image_choices(self):
        media_root = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        choices = []
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.endswith(('jpg', 'jpeg', 'png', 'gif', 'webp ')):
                    choices.append((os.path.join(root, file).replace(media_root, media_url), file))
        return choices

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # widgets = {
        #     'attributes': JSONAttributeWidget,
        # }
        widgets = {
            'image': ImageSelectWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['attributes'].widget = forms.HiddenInput()

    def clean_attributes(self):
        data = self.cleaned_data['attributes']

        return data

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     attributes = self.cleaned_data['attributes']

    #     instance.attributes = attributes
    #     if commit:
    #         instance.save()
    #     return instance
        
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # change_form_template = 'admin/product/change_form.html'
    list_display = ('name', 'category','image_display')
    search_fields = ('name',)
    list_filter = ('category',)
    actions = ['duplicate']

    # formfield_overrides = {
    #     models.JSONField: {'widget': JSONEditorWidget},
    # }

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="aspect-ratio:16/9;" width="100" height="auto"/>', obj.image.url)
        return 'No Image'
    image_display.short_description = 'Image'

    def change_image_link(self, obj):
        url = reverse('admin_image_selector')
        return format_html('<a href="{}" target="_blank">Select Image</a>', url)
    change_image_link.short_description = 'Change Image'

    def display_attributes(self, obj):
        attributes = obj.attributes
        if not attributes:
            return "No attributes"

        # Xây dựng HTML cho việc hiển thị các thuộc tính với nhãn tùy chỉnh
        attribute_lines = []
        for key, value in attributes.items():
            # Ví dụ ánh xạ các thuộc tính với nhãn tùy chỉnh
            custom_labels = {
                'width': 'Width',
                'height': 'Height',
                'weight': 'Weight',
                'color': 'Color',
                'size': 'Size'
            }
            label = custom_labels.get(key, key.capitalize())  # Nhãn tùy chỉnh hoặc mặc định
            attribute_lines.append(f"{label}: {value}")

        return format_html('<br>'.join(attribute_lines))

    display_attributes.short_description = 'Attributes'

    def duplicate(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Xóa khóa chính để tạo đối tượng mới
            obj.save()
        self.message_user(request, "Duplicated.")

    duplicate.short_description = "Duplicate selected items"

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
admin.site.register(Coupon,CouponAdmin)