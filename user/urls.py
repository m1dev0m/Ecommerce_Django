from django.urls import path
from . import views
from .views import LoginAPIView, RegisterAPIView

app_name = 'user'

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('send-verification/', views.send_verification_email, name='send_verification'),
    path('verify-email/', views.verify_email, name='verify_email'),
]