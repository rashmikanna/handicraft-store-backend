from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, TokenObtainPairViewCustom, ProductViewSet

# Router for product-related API endpoints
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # Signup endpoint
    path('token/', TokenObtainPairViewCustom.as_view(), name='token_obtain_pair'),  # Custom login (email-based)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint
    path('', include(router.urls)),  # Product APIs (CRUD)
]
