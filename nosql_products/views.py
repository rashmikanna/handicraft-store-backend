#views for nosql_products, categories

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from .models_nosql import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.exceptions import ValidationError
from bson import ObjectId

#category viewset
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] 

    @action(detail=False, methods=['get'])
    def filter_by_name(self, request):
        name = request.query_params.get('name')
        if name:
            categories = Category.objects(name__icontains=name)
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)
        return Response({"message": "Please provide a category name to filter."}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if not ObjectId.is_valid(pk):
            return Response({"error": "Invalid category ID format"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            category = Category.objects.get(id=ObjectId(pk))
            serializer = self.get_serializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


#product viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny] 

    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValidationError({"message": "Invalid category reference."})
        serializer.save(category=category)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q')
        if query:
            products = Product.objects(name__icontains=query)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({"message": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def filter_by_category(self, request):
        category_name = request.query_params.get('category')
        if category_name:
            category = Category.objects(name__icontains=category_name).first()
            if category:
                products = Product.objects(category=category)
                serializer = self.get_serializer(products, many=True)
                return Response(serializer.data)
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Please provide a category name."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def filter_by_price(self, request):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        try:
            min_price = float(min_price) if min_price else 0
            max_price = float(max_price) if max_price else float('inf')
        except ValueError:
            return Response({"message": "Invalid price range."}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects(price__gte=min_price, price__lte=max_price)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filter_by_availability(self, request):
        available = request.query_params.get('available')
        if available is not None:
            available_bool = available.lower() == 'true'
            products = Product.objects(available=available_bool)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({"message": "Provide 'available' as true or false."}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
    # Validate ObjectId
        if not ObjectId.is_valid(pk):
            return Response({"error": "Invalid product ID format"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            product = Product.objects.get(id=ObjectId(pk))
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)