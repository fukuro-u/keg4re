from django.db import models 
from .product import Product
from .customer import Customer 
from django.utils import timezone
import datetime 

class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address = models.CharField(max_length=50, default='', blank=True) 
    phone = models.CharField(max_length=50, default='', blank=True) 
    date = models.DateField(default=datetime.datetime.today) 
    status = models.BooleanField(default=False) 

    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"

    def update_total(self):
        """
        Update order total.
        """
        self.total = sum(item.subtotal for item in self.order_items.all())
        if self.coupon:
            self.total -= self.coupon.discount
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        """
        Calculator subtotal.
        """
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        """
        Save OrderItem and update order total.
        """
        super().save(*args, **kwargs)
        self.order.update_total()

class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
    ('percent', 'Percentage'),
    ('flat', 'Flat Amount'),
    ]
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percent',
    )

    def __str__(self):
        return f"{self.name} {self.discount} ({self.get_discount_type_display()})"