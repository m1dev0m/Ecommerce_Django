from products.models import Product


def get_cart_items(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        items.append({
            'name': product.name,
            'quantity': quantity,
            'price': float(product.price),
            'subtotal': float(product.price) * quantity
        })
        total_price += product.price * quantity
    return items, total_price

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
