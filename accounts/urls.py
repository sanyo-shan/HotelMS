from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .views import *

urlpatterns = [
    path('member-login/', member_login, name='member-login'),
    path('admin-login/', admin_login, name='admin-login'),
    path('member-register/', member_register, name='member-register'),
    path('admin-register/', admin_register, name='admin-register'),
    path('home/', home, name='home'),
    path('home/1/', home1, name='home1'),
    path('login/', login, name='login'),
    path('token/refresh', TokenRefreshView.as_view, name='token-refresh')
] 