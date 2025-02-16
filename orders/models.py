from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('processing', 'Processing'),('completed', 'Completed'),('cancelled', 'Cancelled'),]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    shipping_address = models.CharField(max_length=255, default='Not specified')

    items = models.ManyToManyField('products.Product', blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"




class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"