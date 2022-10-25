from . import views
from django.urls import path, re_path

app_name = 'TOOSS'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('inventory_list', views.inventory_list, name='inventory_list'),
    path('order_list', views.order_list, name='order_list'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customer/<int:pk>/summary/', views.summary, name='summary'),

]
