from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('producer', 'Producer'),
        ('consumer', 'Consumer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='consumer')
    is_verified = models.BooleanField(default=False)  # Track verification status

# Product category (e.g., sarees, crafts)
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Optional description field

# Each product has name, image, price, description, category, and owner
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    producer = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField(default=0)  # Track stock availability

    def __str__(self):
        return self.name

# Cart item for a user
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)  # Track when item was added

# Order with multiple cart items
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True, null=True)  # Optional shipping address
    payment_status = models.CharField(max_length=20, default='pending')  # Track payment status

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
