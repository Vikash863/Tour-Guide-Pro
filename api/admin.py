from django.contrib import admin
from .models import Destination, Hotel, Cab, Booking, Contact


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'rating', 'created_at']
    search_fields = ['name', 'city', 'state']
    list_filter = ['state', 'rating']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'price_per_night', 'rating', 'available_rooms']
    search_fields = ['name', 'location']
    list_filter = ['rating', 'price_per_night']


@admin.register(Cab)
class CabAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'vehicle_type', 'price_per_km', 'rating', 'available_cars']
    search_fields = ['company_name']
    list_filter = ['vehicle_type', 'rating']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'booking_type', 'total_price', 'booking_status', 'booking_date']
    search_fields = ['user__username', 'booking_type']
    list_filter = ['booking_type', 'booking_status', 'booking_date']
    readonly_fields = ['booking_date']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at']
