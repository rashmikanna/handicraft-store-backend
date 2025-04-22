from rest_framework import serializers
from .models import Product, User, CartItem, Order, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']  # Adjust to your needs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']  # Customize based on what you want to expose

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested Category data
    producer = UserSerializer()     # Nested User data (producer)

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'description', 'category', 'producer', 'stock_quantity']
    
    # Validation to ensure price and stock quantity are valid
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
