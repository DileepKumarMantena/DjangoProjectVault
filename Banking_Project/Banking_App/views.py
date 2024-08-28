from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm,AccountForm
from django.contrib.auth.models import User
from .models import UserRegistrationModel
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserRegistrationModel,Account
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect,get_object_or_404
from django.shortcuts import render
from .forms import CurrencyConverterForm
from .services import CurrencyConverter


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
            return redirect('dashboard')  # Redirect to the home page or any other page
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    if request.method == "POST":
        account_name = request.POST['account_name']
        account_balance = request.POST['account_balance']
        # Assuming the Account model has fields `name` and `balance`
        Account.objects.create(name=account_name, balance=account_balance, user=request.user)
        return redirect('dashboard')

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'accounts': accounts})

def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('dashboard')  # Redirect to the dashboard or another relevant page
    else:
        form = AccountForm()

    return render(request, 'add_account.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def view_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    return render(request, 'view_account.html', {'account': account})

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        account.delete()
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'account': account})

@login_required
def convert_currency(request):
    result = None
    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            from_currency = form.cleaned_data['from_currency']
            to_currency = form.cleaned_data['to_currency']
            converter = CurrencyConverter(api_key=' 95a259e8b3f608ca1125fc6e')
            result = converter.convert(amount, from_currency, to_currency)
    else:
        form = CurrencyConverterForm()

    return render(request,'convert.html', {'form': form, 'result': result})
