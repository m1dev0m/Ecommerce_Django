from django.db import models
from django.conf import settings
from products.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # Один отзыв на товар от пользователя

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"
