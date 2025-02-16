from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'products'

urlpatterns = [

    path('api/', views.ProductListCreateView.as_view(), name='api_product_list'),
    path('api/<int:pk>/', views.ProductDetailView.as_view(), name='api_product_detail'),


    path('', views.product_list_view, name='product_list'),
    path('<int:pk>/', views.product_detail_view, name='product_detail'),
    path('add/', views.add_product_view, name='add_product'),

    path('search/', views.search_products, name='search_products'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)