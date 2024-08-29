from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .models import UserRegistrationModel, Product, Cart, Order
from django.http import HttpResponse


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
            return redirect('dashboard')  # Redirect to the dashboard or home page
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})

    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=cart.get_total_price())
        order.products.set(cart.products.all())
        cart.clear()
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {'cart': cart})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})
