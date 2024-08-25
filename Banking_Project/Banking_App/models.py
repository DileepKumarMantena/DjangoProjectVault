from django.db import models
from django.contrib.auth.models import User

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    class Meta:
        db_table = "User_Table"
