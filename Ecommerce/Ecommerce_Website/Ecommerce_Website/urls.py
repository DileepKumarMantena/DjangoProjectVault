
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ecommerce/', include('Ecommerce_App.urls')),
]