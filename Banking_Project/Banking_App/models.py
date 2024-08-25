from django.db import models
from django.contrib.auth.models import User

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    class Meta:
        db_table = "User_Table"

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    class Meta:
        db_table = "Accounts_Table"