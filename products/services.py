from django.core.cache import cache
from .models import Product

def get_product(product_id):
    key = f"product_{product_id}"
    product = cache.get(key)
    if not product:
        product = Product.objects.get(id=product_id)
        cache.set(key, product, timeout=60 )
    return product
