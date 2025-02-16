from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total = 0

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                price = product.price if product.price else 0

                total += quantity * price
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

            order.total_price = total
            order.save()
        return order

