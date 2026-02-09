from django.contrib import admin
from .models import Destination, Hotel, Booking


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'rating', 'created_at']
    search_fields = ['name', 'city', 'state']
    list_filter = ['state', 'rating']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'price_per_night', 'rating', 'available_rooms']
    search_fields = ['name', 'city', 'state']
    list_filter = ['rating', 'price_per_night']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'booking_type', 'total_price', 'booking_status', 'created_at']
    search_fields = ['user__username', 'booking_type']
    list_filter = ['booking_type', 'booking_status']
