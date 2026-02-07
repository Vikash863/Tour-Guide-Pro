from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, book_hotel
from .views import home, book_hotel, booking_success


from .views import (
    UserViewSet, DestinationViewSet, HotelViewSet,
    CabViewSet, BookingViewSet, ContactViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'destinations', DestinationViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'cabs', CabViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'contacts', ContactViewSet)
urlpatterns = [
    path('', home, name='home'),

    path('book-hotel/', book_hotel, name='book_hotel'),
    path('booking-success/', booking_success, name='booking_success'),

    path('', include(router.urls)),
]

