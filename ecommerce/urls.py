from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('user/', include('user.urls',namespace='user')),
    path('products/', include('products.urls',namespace='products')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls', namespace='reviews')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)