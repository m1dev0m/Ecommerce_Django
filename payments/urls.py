from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:order_id>/', views.process_payment, name='process_payment'),
]
