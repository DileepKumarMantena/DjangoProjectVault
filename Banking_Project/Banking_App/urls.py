from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('add-account/', views.add_account, name='add_account'),
    path('view_account/<int:account_id>/', views.view_account, name='view_account'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),

]
