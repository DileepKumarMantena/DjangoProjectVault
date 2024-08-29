from django.db import models
from django.contrib.auth.models import User

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    class Meta:
        db_table = "User_Table"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')  # Adjust the upload path as needed

    class Meta:
        db_table = 'product_table'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='carts', blank=True)

    class Meta:
        db_table = 'cart_table'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def get_total_price(self):
        """Calculate the total price of all products in the cart."""
        return sum(product.price for product in self.products.all())

    def clear(self):
        """Clear all products from the cart."""
        self.products.clear()

    def __str__(self):
        return f"Cart of {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='orders')

    class Meta:
        db_table = 'order_table'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
