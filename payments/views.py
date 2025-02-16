
from django.shortcuts import render, redirect
from orders.models import Order
from .models import Payment


def process_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    payment = Payment.objects.create(order=order,amount=order.total_price,payment_method='card', status='completed')
    order.status = 'paid'
    order.save()
    return redirect('order_success', order_id=order.id)
