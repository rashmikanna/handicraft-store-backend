from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from .serializers import ProductSerializer
from django.contrib.auth import authenticate

User = get_user_model()

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Ensure all required fields are provided
        if not username or not email or not password:
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TokenObtainPairViewCustom(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')  # not email
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
