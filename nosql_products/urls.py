#urls for nosql_products, categories

from django.urls import path, include
from .views import ProductListView
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, upload_image

#router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)), 
    path('upload-image/', upload_image, name='upload_image'),
    path('products/', ProductListView.as_view(), name='product-list'),
]

