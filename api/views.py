from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token

from .models import HotelBooking

from .db import (
    db, tours_collection, users_collection, bookings_collection, 
    reviews_collection
)
from .models import Destination, Hotel, Cab, Booking, Contact
from .serializers import (
    UserSerializer, UserRegistrationSerializer, DestinationSerializer,
    HotelSerializer, CabSerializer, BookingSerializer, ContactSerializer
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
            # Also save to MongoDB for reference
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
        
        token, created = Token.objects.get_or_create(user=user)
        
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

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request, pk=None):
        """Update user profile"""
        user = self.get_object()
        if user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only update your own profile'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()
        
        # Update in MongoDB
        users_collection.update_one(
            {"user_id": user.id},
            {"$set": {
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "updated_at": datetime.utcnow()
            }}
        )
        
        return Response(
            {'message': 'Profile updated successfully', 'user': UserSerializer(user).data},
            status=status.HTTP_200_OK
        )


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
        
        # Also save to MongoDB for analytics
        tours_collection.insert_one({
            "type": "destination",
            "django_id": instance.id,
            "name": instance.name,
            "city": instance.city,
            "state": instance.state,
            "country": instance.country,
            "rating": instance.rating,
            "average_cost": instance.average_cost,
            "description": instance.description,
            "attractions": instance.attractions,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update destination"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        
        # Update in MongoDB
        tours_collection.update_one(
            {"django_id": instance.id, "type": "destination"},
            {"$set": {
                "name": instance.name,
                "rating": instance.rating,
                "average_cost": instance.average_cost,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete destination"""
        instance = self.get_object()
        id_to_delete = instance.id
        self.perform_destroy(instance)
        
        # Delete from MongoDB
        tours_collection.delete_one({"django_id": id_to_delete, "type": "destination"})
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search destinations by name, city, or country"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Please provide a search query'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        destinations = Destination.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(country__icontains=query)
        )
        serializer = self.get_serializer(destinations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular destinations by rating"""
        destinations = Destination.objects.filter(rating__gte=4).order_by('-rating')[:10]
        serializer = self.get_serializer(destinations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Filter destinations by country"""
        country = request.query_params.get('country', '')
        if not country:
            return Response(
                {'error': 'Please provide a country name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        destinations = Destination.objects.filter(country__icontains=country)
        serializer = self.get_serializer(destinations, many=True)
        return Response(serializer.data)


# ==================== HOTEL VIEWSETS ====================
class HotelViewSet(viewsets.ModelViewSet):
    """CRUD operations for Hotels"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'location', 'destination__name']
    ordering_fields = ['created_at', 'price_per_night', 'rating', 'available_rooms']
    ordering = ['-created_at']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create new hotel"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Save to MongoDB
        tours_collection.insert_one({
            "type": "hotel",
            "django_id": instance.id,
            "name": instance.name,
            "location": instance.location,
            "price_per_night": instance.price_per_night,
            "rating": instance.rating,
            "available_rooms": instance.available_rooms,
            "total_rooms": instance.total_rooms,
            "amenities": instance.amenities,
            "contact": {
                "phone": instance.phone,
                "email": instance.email
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update hotel"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Update in MongoDB
        tours_collection.update_one(
            {"django_id": instance.id, "type": "hotel"},
            {"$set": {
                "name": instance.name,
                "price_per_night": instance.price_per_night,
                "rating": instance.rating,
                "available_rooms": instance.available_rooms,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete hotel"""
        instance = self.get_object()
        id_to_delete = instance.id
        self.perform_destroy(instance)
        
        tours_collection.delete_one({"django_id": id_to_delete, "type": "hotel"})
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search hotels by location or name"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Please provide a search query'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        hotels = Hotel.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
        serializer = self.get_serializer(hotels, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_price_range(self, request):
        """Filter hotels by price range"""
        min_price = request.query_params.get('min_price', 0)
        max_price = request.query_params.get('max_price', 999999)
        
        try:
            hotels = Hotel.objects.filter(
                price_per_night__gte=int(min_price),
                price_per_night__lte=int(max_price)
            )
            serializer = self.get_serializer(hotels, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {'error': 'Invalid price parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get hotels with available rooms"""
        hotels = Hotel.objects.filter(available_rooms__gt=0).order_by('-rating')
        serializer = self.get_serializer(hotels, many=True)
        return Response(serializer.data)


# ==================== CAB VIEWSETS ====================
class CabViewSet(viewsets.ModelViewSet):
    """CRUD operations for Cabs"""
    queryset = Cab.objects.all()
    serializer_class = CabSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['company_name', 'vehicle_type']
    ordering_fields = ['created_at', 'price_per_km', 'rating', 'available_cars']
    ordering = ['-created_at']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create new cab service"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Save to MongoDB
        tours_collection.insert_one({
            "type": "cab",
            "django_id": instance.id,
            "company_name": instance.company_name,
            "vehicle_type": instance.vehicle_type,
            "price_per_km": instance.price_per_km,
            "price_per_hour": instance.price_per_hour,
            "capacity": instance.capacity,
            "rating": instance.rating,
            "available_cars": instance.available_cars,
            "contact": {
                "phone": instance.phone,
                "email": instance.email
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update cab service"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        tours_collection.update_one(
            {"django_id": instance.id, "type": "cab"},
            {"$set": {
                "company_name": instance.company_name,
                "price_per_km": instance.price_per_km,
                "rating": instance.rating,
                "available_cars": instance.available_cars,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete cab service"""
        instance = self.get_object()
        id_to_delete = instance.id
        self.perform_destroy(instance)
        
        tours_collection.delete_one({"django_id": id_to_delete, "type": "cab"})
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def filter(self, request):
        """Filter cabs by type and price"""
        vehicle_type = request.query_params.get('vehicle_type', '')
        min_price = request.query_params.get('min_price', 0)
        max_price = request.query_params.get('max_price', 999999)

        cabs = Cab.objects.all()

        if vehicle_type:
            cabs = cabs.filter(vehicle_type=vehicle_type)
        
        try:
            cabs = cabs.filter(
                price_per_km__gte=float(min_price),
                price_per_km__lte=float(max_price)
            )
        except:
            return Response(
                {'error': 'Invalid price parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(cabs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_company(self, request):
        """Get all vehicles from a specific company"""
        company = request.query_params.get('company', '')
        if not company:
            return Response(
                {'error': 'Please provide a company name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cabs = Cab.objects.filter(company_name__icontains=company)
        serializer = self.get_serializer(cabs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get available cabs"""
        cabs = Cab.objects.filter(available_cars__gt=0).order_by('-rating')
        serializer = self.get_serializer(cabs, many=True)
        return Response(serializer.data)


# ==================== BOOKING VIEWSETS ====================
class BookingViewSet(viewsets.ModelViewSet):
    """CRUD operations for Bookings"""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['booking_date', 'total_price']
    ordering = ['-booking_date']

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user)
        
        # Save to MongoDB for analytics
        booking_data = {
            "user_id": str(request.user.id),
            "username": request.user.username,
            "booking_type": instance.booking_type,
            "django_booking_id": instance.id,
            "total_price": instance.total_price,
            "status": instance.booking_status,
            "payment_status": instance.payment_status,
            "booking_date": datetime.utcnow(),
            "check_in_date": instance.check_in_date.isoformat() if instance.check_in_date else None,
            "check_out_date": instance.check_out_date.isoformat() if instance.check_out_date else None,
            "guests": instance.number_of_guests,
            "rooms": instance.number_of_rooms
        }
        bookings_collection.insert_one(booking_data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update booking"""
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'error': 'You can only update your own bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        bookings_collection.update_one(
            {"django_booking_id": instance.id},
            {"$set": {
                "status": instance.booking_status,
                "payment_status": instance.payment_status,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete booking (only if pending)"""
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'error': 'You can only delete your own bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if instance.booking_status != 'pending':
            return Response(
                {'error': 'Can only delete pending bookings'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        id_to_delete = instance.id
        self.perform_destroy(instance)
        
        bookings_collection.delete_one({"django_booking_id": id_to_delete})
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        if booking.user != request.user:
            return Response(
                {'error': 'You can only cancel your own bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.booking_status in ['cancelled', 'completed']:
            return Response(
                {'error': f'Cannot cancel {booking.booking_status} booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.booking_status = 'cancelled'
        booking.save()
        
        bookings_collection.update_one(
            {"django_booking_id": booking.id},
            {"$set": {"status": "cancelled", "updated_at": datetime.utcnow()}}
        )
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get all bookings for current user"""
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending bookings"""
        bookings = self.get_queryset().filter(booking_status='pending')
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Get confirmed bookings"""
        bookings = self.get_queryset().filter(booking_status='confirmed')
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


# # ==================== CONTACT VIEWSETS ====================
class ContactViewSet(viewsets.ModelViewSet):
    """CRUD operations for Contact Messages"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """Create contact message"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        return Response(
            {
                'message': 'Thank you for contacting us. We will get back to you soon.',
                'contact': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        """Delete contact message"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark contact message as read"""
        contact = self.get_object()
        contact.status = 'read'
        contact.save()
        serializer = self.get_serializer(contact)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_resolved(self, request, pk=None):
        """Mark contact message as resolved"""
        contact = self.get_object()
        contact.status = 'resolved'
        contact.save()
        serializer = self.get_serializer(contact)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        messages = Contact.objects.filter(status='new').order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

# ==================== BOOK HOTEL PAGE ====================
def book_hotel(request):
    hotel_name = request.GET.get('name')

    if request.method == "POST":
        HotelBooking.objects.create(
            hotel_name=request.POST.get("hotel_name"),
            name=request.POST.get("name"),
            checkin=request.POST.get("checkin"),
            checkout=request.POST.get("checkout"),
            guests=request.POST.get("guests"),
            rooms=request.POST.get("rooms"),
        )
        return redirect("booking_success")

    return render(request, "book_hotel.html", {"hotel_name": hotel_name})


# ==================== BOOKING SUCCESS PAGE ====================
def booking_success(request):
    return render(request, "booking_success.html")



# ==================== HOME PAGE ====================
def home(request):
    """Home page with MongoDB tour data"""
    try:
        tours = list(tours_collection.find({}, {"_id": 0}).limit(10))
        destinations_count = Destination.objects.count()
        hotels_count = Hotel.objects.count()
        cabs_count = Cab.objects.count()
        
        context = {
            "tours": tours,
            "stats": {
                "destinations": destinations_count,
                "hotels": hotels_count,
                "cabs": cabs_count
            }
        }
        return render(request, "Home.html", context)
    except Exception as e:
        return render(request, "Home.html", {"error": str(e)})


# ==================== PROFILE PAGE ====================
def profile(request):
    """User profile page"""
    return render(request, "profile.html")
