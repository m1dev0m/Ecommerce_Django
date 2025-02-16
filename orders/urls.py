from django.urls import path
from .views import create_order_view, OrderListView,view_cart,add_to_cart,remove_from_cart,checkout,order_success,order_detail,process_order

app_name = 'orders'

urlpatterns = [
    path('create/<int:product_id>/', create_order_view, name='create_order'),
    path('list/', OrderListView.as_view(), name='list_orders'),

    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order_success/',order_success, name='order_success'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('process/<int:order_id>/', process_order, name='process_order'),
]
