from django.db import models
from orders.models import Order


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('card', 'Credit Card'), ('paypal', 'PayPal')])
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
