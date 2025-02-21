from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save, post_delete

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

from django.db import models
from django.core.cache import cache

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache.delete(f"product_{instance.id}")