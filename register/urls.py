from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('restaurant_dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
