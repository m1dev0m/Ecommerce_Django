from django.core.checks import messages
from django.http import JsonResponse
from rest_framework import generics
from .models import  OrderItem
from .serializers import OrderSerializer
from products.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  CartItem
from .forms import OrderForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Order, Cart
from .forms import PaymentForm
from .utils import get_cart_items, clear_cart
from django.utils.timezone import now

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        item.quantity += quantity
    item.save()

    return redirect('orders:view_cart')





def order_success(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST' and cart_items:
        form = PaymentForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                status="pending",
                created_at=now()
            )
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                for item in cart_items
            ])
            cart.items.all().delete()

            messages.success(request, "Ваш заказ успешно оформлен!")
            return render(request, 'orders/order_success.html')
    else:
        form = PaymentForm()

    return render(request, 'orders/payment_form.html', {'form': form, 'total_price': total_price})


def checkout(request):
    print(">>> CHECKOUT VIEW CALLED <<<")
    cart_items, total_price = get_cart_items(request)
    if not cart_items:
        messages.error(request, "Корзина пуста!")
        return redirect('orders:view_cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                shipping_address=form.cleaned_data['shipping_address'],
                contact_number=form.cleaned_data['contact_number']
            )
            clear_cart(request)
            messages.success(request, f"Заказ {order.id} успешно оформлен!")
            return redirect('orders:order_success')
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('orders:view_cart')

@login_required
def create_order_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        total_price = product.price * quantity

        Order.objects.create(user=request.user, total_price=total_price)
        return redirect('orders:list_orders')

    return render(request, 'orders/create_order.html', {'product': product})


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


def process_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == "pending":
            order.status = "processing"
            order.save()

            return redirect('orders:checkout')
        return JsonResponse({"error": "Order is not in pending status."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)