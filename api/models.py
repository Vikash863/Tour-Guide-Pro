from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    best_time_to_visit = models.CharField(max_length=100)
    attractions = models.JSONField(default=list)
    average_cost = models.IntegerField()
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    price_per_night = models.IntegerField()
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    amenities = models.JSONField(default=list)
    available_rooms = models.IntegerField()
    total_rooms = models.IntegerField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Cab(models.Model):
    VEHICLE_TYPES = [
        ('economy', 'Economy'),
        ('premium', 'Premium'),
        ('luxury', 'Luxury'),
        ('van', 'Van'),
    ]

    company_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    price_per_km = models.FloatField()
    price_per_hour = models.IntegerField()
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='cabs/', blank=True, null=True)
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    available_cars = models.IntegerField()
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - {self.get_vehicle_type_display()}"


class Booking(models.Model):
    BOOKING_TYPES = [
        ('hotel', 'Hotel'),
        ('cab', 'Cab'),
        ('destination', 'Destination'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    number_of_guests = models.IntegerField(null=True, blank=True)
    number_of_rooms = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField()
    payment_status = models.CharField(max_length=20, default='pending')
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.booking_type}"


class Contact(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
