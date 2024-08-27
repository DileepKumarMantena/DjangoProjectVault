
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hospatil/',include("Hospatil_App.urls"))
]
