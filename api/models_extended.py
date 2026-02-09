from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# ==================== SAVED TRIPS / WISHLIST ====================
class SavedTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, null=True, blank=True)
    destination_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='saved_trips/', blank=True, null=True)
    notes = models.TextField(blank=True)
    price_estimate = models.IntegerField(default=0)
    priority = models.IntegerField(default=1)  # 1=high, 2=medium, 3=low
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.destination_name}"


# ==================== PHOTO GALLERY / MEMORIES ====================
class PhotoAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    destination = models.CharField(max_length=100, blank=True)
    is_shared = models.BooleanField(default=False)
    share_link = models.CharField(max_length=100, blank=True, unique=True)
    cover_photo = models.ImageField(upload_to='albums/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def generate_share_link(self):
        import uuid
        self.share_link = str(uuid.uuid4())[:8]
        return self.share_link


class AlbumPhoto(models.Model):
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='album_photos/')
    caption = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    photo_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['photo_date']


# ==================== REVIEWS & RATINGS ====================
class Review(models.Model):
    REVIEW_TYPES = [
        ('destination', 'Destination'),
        ('hotel', 'Hotel'),
        ('cab', 'Cab Service'),
        ('guide', 'Tour Guide'),
        ('package', 'Travel Package'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPES)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)
    cab = models.ForeignKey('Cab', on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey('Package', on_delete=models.CASCADE, null=True, blank=True)
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    
    is_verified = models.BooleanField(default=False)  # Verified booking
    is_approved = models.BooleanField(default=True)
    
    visit_date = models.DateField(null=True, blank=True)
    
    # Engagement metrics
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    like_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.review_type}"


class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='review_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# ==================== CHAT SUPPORT ====================
class ChatConversation(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_chats')
    is_with_guide = models.BooleanField(default=False)
    guide = models.ForeignKey('LocalGuide', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.subject}"


class ChatMessage(models.Model):
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


# ==================== NOTIFICATIONS ====================
class UserNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('booking_confirmation', 'Booking Confirmation'),
        ('booking_reminder', 'Booking Reminder'),
        ('tour_reminder', 'Tour Reminder'),
        ('payment_received', 'Payment Received'),
        ('payment_failed', 'Payment Failed'),
        ('cancellation', 'Cancellation'),
        ('review_request', 'Review Request'),
        ('price_alert', 'Price Alert'),
        ('recommendation', 'Recommendation'),
        ('system', 'System Notification'),
        ('chat', 'Chat Message'),
        ('group_invite', 'Group Trip Invite'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=300, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# ==================== USER PREFERENCES FOR AI ====================
class UserPreference(models.Model):
    BUDGET_CHOICES = [
        ('budget', 'Budget'),
        ('moderate', 'Moderate'),
        ('luxury', 'Luxury'),
    ]

    TRAVEL_STYLES = [
        ('adventure', 'Adventure'),
        ('relaxation', 'Relaxation'),
        ('cultural', 'Cultural'),
        ('family', 'Family'),
        ('solo', 'Solo'),
        ('romantic', 'Romantic'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Basic preferences
    preferred_destinations = models.JSONField(default=list)
    preferred_activities = models.JSONField(default=list)
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='moderate')
    travel_style = models.CharField(max_length=50, choices=TRAVEL_STYLES, default='adventure')
    food_preferences = models.JSONField(default=list)
    accommodation_type = models.CharField(max_length=50, default='hotel')
    
    # Travel info
    passport_country = models.CharField(max_length=50, blank=True)
    frequent_flyer_number = models.CharField(max_length=50, blank=True)
    
    # AI learning
    interests = models.JSONField(default=list)
    disliked_destinations = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences: {self.user.username}"


# ==================== BOOKING PDF / ITINERARY ====================
class BookingItinerary(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itinerary_data = models.JSONField()
    pdf_generated = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='itineraries/', blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Itinerary for {self.booking}"


# ==================== TRAVEL DASHBOARD STATS ====================
class UserTravelStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='travel_stats')
    
    total_trips = models.IntegerField(default=0)
    completed_trips = models.IntegerField(default=0)
    upcoming_trips = models.IntegerField(default=0)
    cancelled_trips = models.IntegerField(default=0)
    
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_distance = models.FloatField(default=0)  # in km
    
    countries_visited = models.IntegerField(default=0)
    states_visited = models.JSONField(default=list)
    
    favorite_destination = models.CharField(max_length=100, blank=True)
    
    last_trip_date = models.DateField(null=True, blank=True)
    next_trip_date = models.DateField(null=True, blank=True)
    
    # Gamification
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badges = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats: {self.user.username}"


# ==================== AI TRAVEL ASSISTANT ====================
class TravelRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=50)  # destination, hotel, activity
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50)
    reason = models.TextField()  # Why recommended
    match_score = models.FloatField()  # 0-100
    is_viewed = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-match_score']


# ==================== CHAT WITH GUIDE ====================
class GuideChatRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]

    tourist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_requests_sent')
    guide = models.ForeignKey('LocalGuide', on_delete=models.CASCADE, related_name='chat_requests_received')
    destination = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist.username} -> {self.guide.full_name}"
