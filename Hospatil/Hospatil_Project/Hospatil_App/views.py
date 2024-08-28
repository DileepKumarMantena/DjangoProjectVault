from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .models import UserRegistrationModel
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserRegistrationModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username_or_email_or_phone = request.POST.get('username_or_email_or_phone')
        password = request.POST.get('password')

        # Try to authenticate by username
        user = authenticate(request, username=username_or_email_or_phone, password=password)
        
        # Try to authenticate by email
        if not user:
            try:
                user = User.objects.get(email=username_or_email_or_phone)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                pass

        # Try to authenticate by phone number
        if not user:
            try:
                user = UserRegistrationModel.objects.get(phone_number=username_or_email_or_phone).user
                user = authenticate(request, username=user.username, password=password)
            except UserRegistrationModel.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other page
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    return render(request, 'profile.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def appointment_view(request):
    return render(request, 'appointment.html')