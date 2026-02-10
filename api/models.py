from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
import uuid
from decimal import Decimal


class TimeStampMixin(models.Model):
    """Abstract base model with timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class UserProfile(TimeStampMixin):
    """Extended user profile with photo and details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not', 'Prefer not to say')], blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_public_profile = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=10, default='en')
    notification_preferences = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserRole(models.TextChoices):
    USER = 'user', 'User'
    ADMIN = 'admin', 'Admin'
    GUIDE = 'guide', 'Local Guide'
    MODERATOR = 'moderator', 'Moderator'


class UserAccount(TimeStampMixin):
    """User account settings and status"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.TextField(blank=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    suspended_until = models.DateTimeField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'user_accounts'
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Destination(TimeStampMixin):
    """Travel destinations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    images = models.JSONField(default=list)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    best_time_to_visit = models.CharField(max_length=200)
    attractions = models.JSONField(default=list)
    activities = models.JSONField(default=list)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='INR')
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    weather_info = models.JSONField(default=dict, blank=True)
    safety_tips = models.JSONField(default=list, blank=True)
    emergency_contacts = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'destinations'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Hotel(TimeStampMixin):
    """Hotel listings"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    images = models.JSONField(default=list)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(default='')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.IntegerField(default=0)
    amenities = models.JSONField(default=list)
    room_types = models.JSONField(default=list)
    available_rooms = models.IntegerField(default=0)
    total_rooms = models.IntegerField(default=0)
    check_in_time = models.TimeField(default='14:00:00')
    check_out_time = models.TimeField(default='11:00:00')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    policies = models.JSONField(default=dict, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hotels'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Booking(TimeStampMixin):
    """Tour booking records"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    BOOKING_TYPES = [
        ('hotel', 'Hotel'),
        ('cab', 'Cab'),
        ('tour', 'Tour Package'),
        ('guide', 'Local Guide'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    booking_reference = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    number_of_guests = models.IntegerField(default=1)
    number_of_rooms = models.IntegerField(default=1)
    guest_details = models.JSONField(default=list, blank=True)
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cancellation_reason = models.TextField(blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    qr_code = models.TextField(blank=True)
    booking_notes = models.TextField(blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    invoice_generated = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.booking_reference}"


class Payment(TimeStampMixin):
    """Payment records"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
        ('wallet', 'Wallet'),
        ('paypal', 'PayPal'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    failure_reason = models.TextField(blank=True)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refunded_at = models.DateTimeField(null=True, blank=True)
    refund_reference = models.CharField(max_length=100, blank=True)
    invoice_url = models.URLField(blank=True)
    receipt_url = models.URLField(blank=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_id}"


class TourHistory(TimeStampMixin):
    """Permanent tour history"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_histories')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    trip_name = models.CharField(max_length=200)
    destination_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    rating_given = models.FloatField(null=True, blank=True)
    review_given = models.BooleanField(default=False)
    photos_count = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    memories = models.JSONField(default=list, blank=True)
    is_favorite = models.BooleanField(default=False)
    share_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'tour_histories'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.trip_name}"


class Wishlist(TimeStampMixin):
    """Saved trips and wishlist"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='INR')
    priority = models.IntegerField(default=1)  # 1=high, 2=medium, 3=low
    target_date = models.DateField(null=True, blank=True)
    is_visited = models.BooleanField(default=False)
    visited_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        db_table = 'wishlists'
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"


class Notification(TimeStampMixin):
    """User notifications"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPES = [
        ('booking', 'Booking'),
        ('payment', 'Payment'),
        ('reminder', 'Reminder'),
        ('promotion', 'Promotion'),
        ('system', 'System'),
        ('review', 'Review'),
        ('referral', 'Referral'),
        ('price_drop', 'Price Drop'),
        ('weather', 'Weather Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    link = models.URLField(blank=True)
    link_text = models.CharField(max_length=100, blank=True)
    data = models.JSONField(default=dict, blank=True)
    priority = models.IntegerField(default=1)  # 1=high, 2=normal, 3=low
    expires_at = models.DateTimeField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    push_sent = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class TravelGallery(TimeStampMixin):
    """User travel photos and memories"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_items')
    tour_history = models.ForeignKey(TourHistory, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', null=True, blank=True)
    image_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_taken = models.DateField()
    is_public = models.BooleanField(default=False)
    likes_count = models.IntegerField(default=0)
    tags = models.JSONField(default=list, blank=True)
    album = models.CharField(max_length=100, blank=True)
    cloudinary_public_id = models.CharField(max_length=200, blank=True)
    size_bytes = models.BigIntegerField(default=0)
    
    class Meta:
        db_table = 'travel_gallery'
        ordering = ['-date_taken']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Review(TimeStampMixin):
    """User reviews and ratings"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='review')
    tour_history = models.ForeignKey(TourHistory, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
   