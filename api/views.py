from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token as AuthToken

from .models import Booking

from .db import (
    db, tours_collection, users_collection, bookings_collection, 
    reviews_collection
)
from .models import Destination, Hotel
from .serializers import (
    UserSerializer, UserRegistrationSerializer, DestinationSerializer,
    HotelSerializer, BookingSerializer
)


# ==================== AUTHENTICATION VIEWSETS ====================
class UserViewSet(viewsets.ModelViewSet):
    """User authentication and profile management"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            users_collection.insert_one({
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            return Response(
                {
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login with token authentication"""
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
        
        token, created = AuthToken.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """User logout"""
        try:
            request.user.auth_token.delete()
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Logout failed'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ==================== DESTINATION VIEWSETS ====================
class DestinationViewSet(viewsets.ModelViewSet):
    """CRUD operations for Destinations"""
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'city', 'state', 'country']
    ordering_fields = ['created_at', 'rating', 'average_cost']
    ordering = ['-created_at']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create new destination - stores in both Django and MongoDB"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        tours_collection.insert_one({
            "type": "destination",
            "django_id": str(instance.id),
            "name": instance.name,
            "city": instance.city,
            "state": instance.state,
            "country": instance.country,
            "rating": instance.rating,
            "average_cost": str(instance.average_cost),
            "created_at": datetime.utcnow(),
        })
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Delete destination"""
        instance = self.get_object()
        id_to_delete = instance.id
        self.perform_destroy(instance)
        tours_collection.delete_one({"django_id": str(id_to_delete), "type": "destination"})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular destinations by rating"""
        destinations = Destination.objects.filter(rating__gte=4).order_by('-rating')[:10]
        serializer = self.get_serializer(destinations, many=True)
        return Response(serializer.data)


# ==================== HOTEL VIEWSETS ====================
class HotelViewSet(viewsets.ModelViewSet):
    """CRUD operations for Hotels"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'city']
    ordering_fields = ['created_at', 'price_per_night', 'rating']
    ordering = ['-created_at']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create new hotel"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        tours_collection.insert_one({
            "type": "hotel",
            "django_id": str(instance.id),
            "name": instance.name,
            "city": instance.city,
            "price_per_night": str(instance.price_per_night),
            "rating": instance.rating,
            "created_at": datetime.utcnow(),
        })
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Delete hotel"""
        instance = self.get_object()
        id_to_delete = instance.id
        self.perform_destroy(instance)
        tours_collection.delete_one({"django_id": str(id_to_delete), "type": "hotel"})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get hotels with available rooms"""
        hotels = Hotel.objects.filter(available_rooms__gt=0).order_by('-rating')
        serializer = self.get_serializer(hotels, many=True)
        return Response(serializer.data)


# ==================== BOOKING VIEWSETS ====================
class BookingViewSet(viewsets.ModelViewSet):
    """CRUD operations for Bookings"""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'total_price']
    ordering = ['-created_at']

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user)
        
        booking_data = {
            "user_id": str(request.user.id),
            "booking_type": instance.booking_type,
            "django_booking_id": str(instance.id),
            "total_price": str(instance.total_price),
            "status": instance.booking_status,
            "booking_date": datetime.utcnow(),
        }
        bookings_collection.insert_one(booking_data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get all bookings for current user"""
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


# ==================== BOOK HOTEL PAGE ====================
def book_hotel(request):
    """Hotel booking page"""
    hotel_name = request.GET.get('name', '')
    
    if request.method == "POST":
        # Redirect to booking success for now
        return redirect("booking_success")

    return render(request, "book_hotel.html", {"hotel_name": hotel_name})


# ==================== BOOKING SUCCESS PAGE ====================
def booking_success(request):
    """Booking success page"""
    return render(request, "booking_success.html")


# ==================== HOME PAGE ====================
def home(request):
    """Home page with MongoDB tour data"""
    try:
        tours = list(tours_collection.find({}, {"_id": 0}).limit(10))
        try:
            destinations_count = Destination.objects.count()
        except:
            destinations_count = 0
        try:
            hotels_count = Hotel.objects.count()
        except:
            hotels_count = 0
        
        context = {
            "tours": tours,
            "stats": {
                "destinations": destinations_count,
                "hotels": hotels_count,
                "cabs": 0
            }
        }
        return render(request, "Home.html", context)
    except Exception as e:
        return render(request, "Home.html", {"error": str(e)})


# ==================== PROFILE PAGE ====================
def profile(request):
    """User profile page"""
    return render(request, "profile.html")
