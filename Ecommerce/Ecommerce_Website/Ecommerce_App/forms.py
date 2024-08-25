from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserRegistrationModel

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if UserRegistrationModel.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("This phone number is already registered.")
        return phone_number

    def save(self, commit=True):
        # Save the User instance first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create and save the UserRegistrationModel instance
            UserRegistrationModel.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number']
            )
        return user
