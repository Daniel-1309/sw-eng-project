from django.contrib import admin
from django.urls import path
from order import views
from django.contrib.auth.views import LoginView
from order.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the custom login view
    path('signup/', views.sign_up, name='signup'),
    path('create_order/', views.create_order, name='create_order'),
    path('api/orders/', views.orders_dashboard_data, name='orders_dashboard_data'),
]
