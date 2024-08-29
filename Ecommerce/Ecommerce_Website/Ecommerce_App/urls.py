from django.urls import path
from .views import (
    register, user_login, user_logout, dashboard, product_list, product_detail,
    add_to_cart, cart_detail, checkout, order_confirmation, order_history
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('order_history/', order_history, name='order_history'),
]
