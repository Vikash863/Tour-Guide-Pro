from django.urls import path, include
from django.views.i18n import set_language
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .views import (
    home, book_hotel, booking_success, profile,
    UserViewSet, DestinationViewSet, HotelViewSet,
    CabViewSet, BookingViewSet, ContactViewSet
)

# ----------------------
# API Router
# ----------------------
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'destinations', DestinationViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'cabs', CabViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'contacts', ContactViewSet)

# Custom login view that returns token + user data
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def login_user(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'message': 'Login successful',
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }, status=status.HTTP_200_OK)

# Simple registration view
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    if not username or not email or not password:
        return Response(
            {'error': 'Username, email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already registered'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    
    return Response({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }, status=status.HTTP_201_CREATED)

# ----------------------
# URL Patterns
# ----------------------
urlpatterns = [
    # Home & Booking Pages
    path('', home, name='home'),
    path('book-hotel/', book_hotel, name='book_hotel'),
    path('booking-success/', booking_success, name='booking_success'),
    path('profile/', profile, name='profile'),

    # Auth endpoints
    path('api/register/', register_user, name='register'),
    path('api/auth/login/', login_user, name='api_login'),

    # Include API router URLs
    path('api/', include(router.urls)),

    # Language switcher
    path('set-language/', set_language, name='set_language'),
]
