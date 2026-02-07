from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home

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
    # Homepage (MongoDB)
    path('', home, name='home'),

    # All APIs (router automatically prefixed with /api/ from main urls.py)
    path('', include(router.urls)),
]

