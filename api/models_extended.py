"""
Extended Models for Tour Guide Pro - All 15 Features
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


# ==================== 1) SMART TRIP ASSISTANT (AI) ====================
class TripPlan(models.Model):
    """AI-generated trip plans based on user preferences"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, null=True, blank=True)
    destination_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.IntegerField()
    interests = models.JSONField(default=list)  # e.g., ['adventure', 'culture', 'food']
    trip_type = models.CharField(max_length=50)  # solo, family, couple, group
    days = models.IntegerField()
    itinerary = models.JSONField()  # Detailed day-by-day plan
    ai_generated = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default='draft')  # draft, active, completed, cancelled
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.destination_name}"


class TripPreference(models.Model):
    """User preferences for AI recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    preferred_destinations = models.JSONField(default=list)
    preferred_activities = models.JSONField(default=list)
    budget_range = models.CharField(max_length=50)  # budget, moderate, luxury
    travel_style = models.CharField(max_length=50)  # adventurous, relaxing, cultural
    food_preferences = models.JSONField(default=list)
    accommodation_type = models.CharField(max_length=50)  # hotel, hostel, resort, homestay
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences: {self.user.username}"


# ==================== 2) TRIP BUDGET CALCULATOR ====================
class BudgetTracker(models.Model):
    """Track trip expenses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, null=True, blank=True)
    trip_name = models.CharField(max_length=100)
    total_budget = models.IntegerField()
    transport_cost = models.IntegerField(default=0)
    hotel_cost = models.IntegerField(default=0)
    food_cost = models.IntegerField(default=0)
    activities_cost = models.IntegerField(default=0)
    shopping_cost = models.IntegerField(default=0)
    miscellaneous_cost = models.IntegerField(default=0)
    currency = models.CharField(max_length=10, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trip_name} - {self.user.username}"

    @property
    def total_spent(self):
        return (self.transport_cost + self.hotel_cost + self.food_cost + 
                self.activities_cost + self.shopping_cost + self.miscellaneous_cost)

    @property
    def remaining_budget(self):
        return self.total_budget - self.total_spent


class DailyExpense(models.Model):
    """Daily expense tracking"""
    budget_tracker = models.ForeignKey(BudgetTracker, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=50)  # transport, food, activities, etc.
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.description}"


class CurrencyRate(models.Model):
    """Currency exchange rates"""
    currency_code = models.CharField(max_length=10, unique=True)
    currency_name = models.CharField(max_length=50)
    rate_to_inr = models.FloatField()  # 1 unit = X INR
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency_code} ({self.currency_name})"


# ==================== 3 & 9) NEARBY PLACES & WEATHER ====================
class SavedPlace(models.Model):
    """User saved nearby places"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=200)  # Google Maps place ID
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    place_type = models.CharField(max_length=50)  # tourist_attraction, restaurant, hotel, etc.
    distance = models.FloatField()  # in km
    rating = models.FloatField(default=0)
    photo_url = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['distance']

    def __str__(self):
        return self.name


class WeatherCache(models.Model):
    """Cached weather data for locations"""
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10)
    wind_speed = models.FloatField()
    forecast_date = models.DateField()
    cached_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['city', 'forecast_date']

    def __str__(self):
        return f"{self.city} - {self.forecast_date}"


# ==================== 4) OFFLINE TRAVEL GUIDE ====================
class OfflineGuide(models.Model):
    """Offline guides for destinations"""
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    pdf_file = models.FileField(upload_to='offline_guides/', null=True, blank=True)
    map_image = models.ImageField(upload_to='offline_maps/', null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    version = models.CharField(max_length=20, default='1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.destination.name} - {self.title}"


class TripChecklist(models.Model):
    """Trip checklist items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    items = models.JSONField(default=list)  # List of checklist items
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ==================== 5) TRAVEL MEMORY SCRAPBOOK ====================
class TravelMemory(models.Model):
    """Travel photos and memories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    visit_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class TravelPhoto(models.Model):
    """Photos for travel memories"""
    memory = models.ForeignKey(TravelMemory, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='travel_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.memory.title}"


class TravelNote(models.Model):
    """Notes for travel memories"""
    memory = models.ForeignKey(TravelMemory, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.memory.title}"


# ==================== 6) GROUP TRIP PLANNER ====================
class GroupTrip(models.Model):
    """Group trip planning"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_trips')
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='planning')  # planning, confirmed, completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Group trip to {self.destination}"


class GroupTripMember(models.Model):
    """Members of group trips"""
    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    group_trip = models.ForeignKey(GroupTrip, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    invited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['group_trip', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.group_trip.destination}"


class GroupPoll(models.Model):
    """Polls for group trip decisions"""
    group_trip = models.ForeignKey(GroupTrip, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    poll_type = models.CharField(max_length=50)  # date, destination, activity
    options = models.JSONField()  # List of options
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.question


class PollVote(models.Model):
    """Votes on polls"""
    poll = models.ForeignKey(GroupPoll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=100)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['poll', 'user']

    def __str__(self):
        return f"{self.user.username} voted: {self.selected_option}"


class GroupExpense(models.Model):
    """Group expense tracking"""
    group_trip = models.ForeignKey(GroupTrip, on_delete=models.CASCADE, related_name='expenses')
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    split_type = models.CharField(max_length=20, default='equal')  # equal, percentage, exact
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"


class ExpenseSplit(models.Model):
    """Individual splits for group expenses"""
    expense = models.ForeignKey(GroupExpense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} owes {self.amount}"


# ==================== 7) RECOMMENDATION ENGINE ====================
class UserRecommendation(models.Model):
    """Personalized recommendations for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=50)  # destination, hotel, activity
    item_id = models.IntegerField()  # ID of recommended item
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50)
    reason = models.TextField()  # Why this is recommended
    score = models.FloatField()  # Relevance score
    is_viewed = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.item_name}"


class TrendingDestination(models.Model):
    """Trending destinations"""
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    trend_score = models.FloatField(default=0)
    booking_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    trend_direction = models.CharField(max_length=20, default='up')  # up, down, stable
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-trend_score']

    def __str__(self):
        return f"{self.destination.name} (score: {self.trend_score})"


# ==================== 8) SMART NOTIFICATIONS ====================
class Notification(models.Model):
    """User notifications"""
    TYPES = [
        ('price_drop', 'Price Drop'),
        ('weather_alert', 'Weather Alert'),
        ('booking_reminder', 'Booking Reminder'),
        ('trip_update', 'Trip Update'),
        ('group_invite', 'Group Invite'),
        ('recommendation', 'Recommendation'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class PriceAlert(models.Model):
    """Price drop alerts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=50)  # hotel, flight, package
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=100)
    target_price = models.IntegerField()
    current_price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Alert: {self.item_name} below {self.target_price}"


# ==================== 10) SAFETY & EMERGENCY ====================
class EmergencyInfo(models.Model):
    """Emergency numbers and safety info for destinations"""
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    country_code = models.CharField(max_length=10)
    police = models.CharField(max_length=20)
    ambulance = models.CharField(max_length=20)
    fire = models.CharField(max_length=20)
    tourist_police = models.CharField(max_length=20, blank=True)
    embassy_phone = models.CharField(max_length=20, blank=True)
    embassy_address = models.TextField(blank=True)
    general_safety_tips = models.JSONField(default=list)
    health_advisories = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Emergency Info: {self.destination.name}"


class SafeArea(models.Model):
    """Safe areas in a destination"""
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    area_name = models.CharField(max_length=100)
    description = models.TextField()
    safety_rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_recommended = models.BooleanField(default=True)
    area_type = models.CharField(max_length=50)  # accommodation, dining, sightseeing

    def __str__(self):
        return f"{self.area_name} - {self.destination.name}"


class TravelAdvisory(models.Model):
    """Travel advisories"""
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    advisory_level = models.CharField(max_length=20)  # normal, caution, warning, avoid
    title = models.CharField(max_length=200)
    description = models.TextField()
    issued_by = models.CharField(max_length=100)
    valid_from = models.DateField()
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.advisory_level}"


# ==================== 11) QR BASED TICKETS ====================
class QRTicket(models.Model):
    """QR code tickets for bookings"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, null=True, blank=True)
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, null=True, blank=True)
    ticket_type = models.CharField(max_length=50)  # hotel, attraction, transport, event
    ticket_id = models.CharField(max_length=100, unique=True)
    qr_code = models.TextField()  # QR code data URL
    qr_image = models.ImageField(upload_to='qr_tickets/', null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    scan_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket: {self.ticket_id}"


# ==================== 12) GAMIFICATION ====================
class UserBadge(models.Model):
    """User earned badges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=100)
    badge_description = models.TextField()
    badge_icon = models.CharField(max_length=200, blank=True)  # Icon URL or class
    badge_type = models.CharField(max_length=50)  # travel, achievement, milestone
    earned_at = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'badge_name']

    def __str__(self):
        return f"{self.user.username} - {self.badge_name}"


class UserPoints(models.Model):
    """User points for gamification"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='points')
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    trips_completed = models.IntegerField(default=0)
    countries_visited = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0)  # in km
    total_spent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_points} points"

    def add_points(self, points):
        self.total_points += points
        self.level = (self.total_points // 1000) + 1
        self.save()

    def calculate_level(self):
        return (self.total_points // 1000) + 1


class PointTransaction(models.Model):
    """Point transactions history"""
    TRANSACTION_TYPES = [
        ('earned', 'Earned'),
        ('redeemed', 'Redeemed'),
        ('bonus', 'Bonus'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type}: {self.points}"


class Leaderboard(models.Model):
    """Leaderboard entries"""
    PERIODS = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=20, choices=PERIODS)
    rank = models.IntegerField()
    points = models.IntegerField()
    trips_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'period']

    def __str__(self):
        return f"{self.user.username} - #{self.rank} ({self.period})"


# ==================== 13) COMMUNITY FORUM ====================
class ForumPost(models.Model):
    """Community forum posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)  # question, discussion, tip, review, guide
    tags = models.JSONField(default=list)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ForumComment(models.Model):
    """Comments on forum posts"""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_accepted = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class ForumVote(models.Model):
    """Votes on forum posts/comments"""
    VOTE_TYPES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20)  # post, comment
    content_id = models.IntegerField()
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'content_type', 'content_id']

    def __str__(self):
        return f"{self.user.username} {self.vote_type}voted content {self.content_id}"


# ==================== 14) LOCAL GUIDE MARKETPLACE ====================
class LocalGuide(models.Model):
    """Local guide profiles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guide_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    bio = models.TextField()
    languages = models.JSONField(default=list)  # List of languages
    locations = models.JSONField(default=list)  # Cities/regions they cover
    specializations = models.JSONField(default=list)  # Food, history, adventure, etc.
    experience_years = models.IntegerField(default=0)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.IntegerField(default=0)
    hourly_rate = models.IntegerField()
    daily_rate = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='guides/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class GuideBooking(models.Model):
    """Bookings for local guides"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    guide = models.ForeignKey(LocalGuide, on_delete=models.CASCADE)
    tourist = models.ForeignKey(User, on_delete=models.CASCADE)
    tour_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    hours_per_day = models.IntegerField(default=8)
    total_hours = models.IntegerField()
    hourly_rate = models.IntegerField()
    total_price = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist.username} - {self.guide.full_name}"


class GuideReview(models.Model):
    """Reviews for local guides"""
    guide = models.ForeignKey(LocalGuide, on_delete=models.CASCADE, related_name='reviews')
    tourist = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(GuideBooking, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['guide', 'tourist']

    def __str__(self):
        return f"Review for {self.guide.full_name}"


class GuideChat(models.Model):
    """Chat messages with guides"""
    guide = models.ForeignKey(LocalGuide, on_delete=models.CASCADE)
    tourist = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sender_type = models.CharField(max_length=20)  # guide, tourist
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.tourist.username} - {self.guide.full_name}"


# ==================== 15) ADMIN AUTOMATION ====================
class PriceHistory(models.Model):
    """Price history tracking"""
    item_type = models.CharField(max_length=50)  # hotel, destination, package
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=100)
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    change_type = models.CharField(max_length=20)  # increase, decrease
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name}: {self.old_price} -> {self.new_price}"


class Package(models.Model):
    """Travel packages"""
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    duration_days = models.IntegerField()
    base_price = models.IntegerField()
    max_persons = models.IntegerField()
    included_services = models.JSONField(default=list)
    excluded_services = models.JSONField(default=list)
    itinerary = models.JSONField()
    images = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_packages')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_packages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PackageApproval(models.Model):
    """Package approval workflow"""
    ACTION_TYPES = [
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('revise', 'Requested Revision'),
    ]

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.package.name} - {self.action_type}"


class UserModeration(models.Model):
    """User moderation actions"""
    MODERATION_TYPES = [
        ('warning', 'Warning'),
        ('suspend', 'Suspension'),
        ('ban', 'Ban'),
        ('verify', 'Verify'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moderation_type = models.CharField(max_length=20, choices=MODERATION_TYPES)
    reason = models.TextField()
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='moderation_actions')
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.moderation_type}"


class UserReport(models.Model):
    """User reports"""
    REPORT_TYPES = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('fake', 'Fake Profile'),
        ('inappropriate', 'Inappropriate Content'),
        ('scam', 'Scam'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_filed')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.reporter.username} on {self.reported_user.username}"
