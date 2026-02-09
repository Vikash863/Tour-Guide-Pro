from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DestinationViewSet, HotelViewSet, BookingViewSet

# ----------------------
# API Router
# ----------------------
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'destinations', DestinationViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')

# ----------------------
# URL Patterns
# ----------------------
urlpatterns = [
    path('', include(router.urls)),
]
