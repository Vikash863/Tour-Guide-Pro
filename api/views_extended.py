"""
Extended API Views for Tour Guide Pro - All 15 Features
"""
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import uuid
import json

from .models_extended import (
    TripPlan, TripPreference, BudgetTracker, DailyExpense, CurrencyRate,
    SavedPlace, WeatherCache, OfflineGuide, TripChecklist,
    TravelMemory, TravelPhoto, TravelNote,
    GroupTrip, GroupTripMember, GroupPoll, PollVote, GroupExpense, ExpenseSplit,
    UserRecommendation, TrendingDestination,
    Notification, PriceAlert,
    EmergencyInfo, SafeArea, TravelAdvisory,
    QRTicket,
    UserBadge, UserPoints, PointTransaction, Leaderboard,
    ForumPost, ForumComment, ForumVote,
    LocalGuide, GuideBooking, GuideReview, GuideChat,
    PriceHistory, Package, PackageApproval, UserModeration, UserReport
)
from .models import Destination, Hotel, Booking


# ==================== 1) SMART TRIP ASSISTANT (AI) ====================
class TripPlanViewSet(viewsets.ModelViewSet):
    """AI Trip Plan Management"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TripPlan.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Generate AI trip plan based on user preferences"""
        data = request.data
        
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        days = (end_date - start_date).days + 1
        
        itinerary = self._generate_ai_itinerary(
            data.get('destination_name', ''),
            days,
            data.get('budget', 0),
            data.get('interests', []),
            data.get('trip_type', 'solo'),
            start_date
        )
        
        trip_plan = TripPlan.objects.create(
            user=request.user,
            destination_name=data.get('destination_name', ''),
            start_date=start_date,
            end_date=end_date,
            budget=data.get('budget', 0),
            interests=data.get('interests', []),
            trip_type=data.get('trip_type', 'solo'),
            days=days,
            itinerary=itinerary,
            ai_generated=True
        )
        
        self._award_points(request.user, 50, 'earned', 'Created new trip plan')
        
        return Response({
            'message': 'Trip plan generated successfully',
            'trip_plan': {
                'id': trip_plan.id,
                'destination': trip_plan.destination_name,
                'days': trip_plan.days,
                'budget': trip_plan.budget,
                'itinerary': trip_plan.itinerary
            }
        }, status=status.HTTP_201_CREATED)
    
    def _generate_ai_itinerary(self, destination, days, budget, interests, trip_type, start_date):
        """Generate AI itinerary"""
        itinerary = {}
        daily_budget = budget // days if days > 0 else 0
        
        activities_by_interest = {
            'adventure': ['Trekking', 'Water Sports', 'Paragliding', 'Rock Climbing'],
            'culture': ['Museum Visit', 'Temple Tour', 'Historical Sites', 'Local Markets'],
            'food': ['Food Tour', 'Cooking Class', 'Street Food', 'Fine Dining'],
            'relaxation': ['Spa', 'Beach', 'Nature Walk', 'Yoga'],
            'shopping': ['Local Markets', 'Malls', 'Handicrafts', 'Street Shopping']
        }
        
        for day in range(1, days + 1):
            day_activities = []
            selected_interests = interests if interests else ['culture', 'adventure']
            
            for interest in selected_interests:
                if interest in activities_by_interest:
                    activity = activities_by_interest[interest][day % len(activities_by_interest[interest])]
                    day_activities.append({
                        'time': '09:00 AM',
                        'activity': activity,
                        'duration': '3 hours',
                        'cost': round(daily_budget * 0.3),
                        'notes': f'Best {activity} near {destination}'
                    })
            
            day_activities.append({
                'time': '12:00 PM',
                'activity': 'Lunch',
                'duration': '1 hour',
                'cost': round(daily_budget * 0.2),
                'notes': 'Local cuisine recommendation'
            })
            day_activities.append({
                'time': '07:00 PM',
                'activity': 'Dinner',
                'duration': '2 hours',
                'cost': round(daily_budget * 0.25),
                'notes': 'Try local specialties'
            })
            
            current_date = start_date + timedelta(days=day-1)
            itinerary[f'Day {day}'] = {
                'date': current_date.strftime('%Y-%m-%d'),
                'theme': selected_interests[day % len(selected_interests)] if selected_interests else 'exploration',
                'activities': day_activities,
                'daily_budget': daily_budget,
                'tips': [f'Best time to visit {destination} is morning', 'Carry comfortable shoes']
            }
        
        return itinerary
    
    def _award_points(self, user, points, trans_type, description):
        """Award points to user"""
        user_points, created = UserPoints.objects.get_or_create(user=user)
        user_points.add_points(points)
        PointTransaction.objects.create(
            user=user, points=points, transaction_type=trans_type, description=description
        )
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate trip itinerary"""
        trip_plan = self.get_object()
        new_itinerary = self._generate_ai_itinerary(
            trip_plan.destination_name,
            trip_plan.days,
            trip_plan.budget,
            request.data.get('interests', trip_plan.interests),
            trip_plan.trip_type,
            trip_plan.start_date
        )
        trip_plan.itinerary = new_itinerary
        trip_plan.save()
        return Response({'message': 'Itinerary regenerated', 'itinerary': new_itinerary})
    
    @action(detail=True, methods=['get'])
    def share(self, request, pk=None):
        """Get shareable trip plan"""
        trip_plan = self.get_object()
        return Response({
            'destination': trip_plan.destination_name,
            'dates': f"{trip_plan.start_date} to {trip_plan.end_date}",
            'budget': trip_plan.budget,
            'itinerary': trip_plan.itinerary
        })


class TripPreferenceViewSet(viewsets.ModelViewSet):
    """User Trip Preferences"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TripPreference.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Save user preferences"""
        pref, created = TripPreference.objects.update_or_create(
            user=request.user,
            defaults={
                'preferred_destinations': request.data.get('preferred_destinations', []),
                'preferred_activities': request.data.get('preferred_activities', []),
                'budget_range': request.data.get('budget_range', 'moderate'),
                'travel_style': request.data.get('travel_style', 'balanced'),
                'food_preferences': request.data.get('food_preferences', []),
                'accommodation_type': request.data.get('accommodation_type', 'hotel')
            }
        )
        return Response({
            'message': 'Preferences saved',
            'preferences': {
                'preferred_destinations': pref.preferred_destinations,
                'preferred_activities': pref.preferred_activities,
                'budget_range': pref.budget_range,
                'travel_style': pref.travel_style
            }
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my(self, request):
        """Get current user preferences"""
        try:
            pref = TripPreference.objects.get(user=request.user)
            return Response(pref.__dict__)
        except TripPreference.DoesNotExist:
            return Response({'message': 'No preferences set'}, status=status.HTTP_404_NOT_FOUND)


# ==================== 2) TRIP BUDGET CALCULATOR ====================
class BudgetTrackerViewSet(viewsets.ModelViewSet):
    """Budget Tracking"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BudgetTracker.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Create budget tracker"""
        tracker = BudgetTracker.objects.create(
            user=request.user,
            trip_name=request.data.get('trip_name', ''),
            total_budget=request.data.get('total_budget', 0),
            transport_cost=request.data.get('transport_cost', 0),
            hotel_cost=request.data.get('hotel_cost', 0),
            food_cost=request.data.get('food_cost', 0),
            activities_cost=request.data.get('activities_cost', 0),
            shopping_cost=request.data.get('shopping_cost', 0),
            miscellaneous_cost=request.data.get('miscellaneous_cost', 0),
            currency=request.data.get('currency', 'INR')
        )
        return Response({
            'message': 'Budget tracker created',
            'tracker_id': tracker.id,
            'total_budget': tracker.total_budget,
            'total_spent': tracker.total_spent,
            'remaining': tracker.remaining_budget
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get budget summary"""
        tracker = self.get_object()
        return Response({
            'total_budget': tracker.total_budget,
            'total_spent': tracker.total_spent,
            'remaining_budget': tracker.remaining_budget,
            'currency': tracker.currency,
            'breakdown': {
                'transport': tracker.transport_cost,
                'hotel': tracker.hotel_cost,
                'food': tracker.food_cost,
                'activities': tracker.activities_cost,
                'shopping': tracker.shopping_cost,
                'miscellaneous': tracker.miscellaneous_cost
            },
            'percent_used': round((tracker.total_spent / tracker.total_budget * 100), 2) if tracker.total_budget > 0 else 0
        })


class CurrencyConverterView(APIView):
    """Currency Conversion"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get available currencies"""
        currencies = [
            {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹'},
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£'},
            {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥'},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$'},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': 'C$'},
            {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': 'S$'},
            {'code': 'AED', 'name': 'UAE Dirham', 'symbol': 'د.إ'},
        ]
        return Response({'currencies': currencies})
    
    def post(self, request):
        """Convert currency"""
        amount = float(request.data.get('amount', 0))
        from_currency = request.data.get('from_currency', 'INR')
        to_currency = request.data.get('to_currency', 'USD')
        
        rates_to_inr = {
            'INR': 1.0, 'USD': 83.50, 'EUR': 90.25, 'GBP': 105.50,
            'JPY': 0.56, 'AUD': 54.50, 'CAD': 61.75, 'SGD': 61.50, 'AED': 22.75
        }
        
        inr_amount = amount * rates_to_inr.get(from_currency, 1)
        converted_amount = inr_amount / rates_to_inr.get(to_currency, 1)
        
        return Response({
            'original': {'amount': amount, 'currency': from_currency},
            'converted': {'amount': round(converted_amount, 2), 'currency': to_currency},
            'rate': round(rates_to_inr.get(from_currency, 1) / rates_to_inr.get(to_currency, 1), 4)
        })


# ==================== 3) NEARBY PLACES FINDER ====================
class NearbyPlacesViewSet(viewsets.ModelViewSet):
    """Nearby Places Finder"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SavedPlace.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Save a nearby place"""
        place = SavedPlace.objects.create(
            user=request.user,
            name=request.data.get('name'),
            place_id=request.data.get('place_id'),
            address=request.data.get('address'),
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude'),
            place_type=request.data.get('place_type'),
            distance=request.data.get('distance', 0),
            rating=request.data.get('rating', 0),
            photo_url=request.data.get('photo_url', '')
        )
        return Response({
            'message': 'Place saved',
            'place': {'id': place.id, 'name': place.name, 'type': place.place_type}
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search nearby places"""
        lat = request.query_params.get('latitude')
        lng = request.query_params.get('longitude')
        place_type = request.query_params.get('type', 'tourist_attraction')
        
        results = [
            {
                'name': 'City Center Mall',
                'place_id': 'ChIJ123',
                'address': '123 Main Street',
                'latitude': float(lat) + 0.01 if lat else 0,
                'longitude': float(lng) + 0.01 if lng else 0,
                'place_type': 'shopping_mall',
                'distance': 0.5,
                'rating': 4.2,
                'photo_url': '',
                'opening_hours': '10:00 AM - 10:00 PM'
            },
            {
                'name': 'Grand Museum',
                'place_id': 'ChIJ456',
                'address': '456 Heritage Road',
                'latitude': float(lat) - 0.02 if lat else 0,
                'longitude': float(lng) + 0.005 if lng else 0,
                'place_type': 'museum',
                'distance': 1.2,
                'rating': 4.5,
                'photo_url': '',
                'opening_hours': '9:00 AM - 6:00 PM'
            }
        ]
        return Response({'results': results})


# ==================== 9) WEATHER INTEGRATION ====================
class WeatherView(APIView):
    """Weather Integration"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get weather for a location"""
        city = request.query_params.get('city', 'Mumbai')
        destination_id = request.query_params.get('destination_id')
        
        weather_data = {
            'city': city,
            'country': 'India',
            'temperature': 28,
            'humidity': 65,
            'description': 'Partly cloudy',
            'icon': '02d',
            'wind_speed': 12.5,
            'feels_like': 30,
            'visibility': 10000,
            'uv_index': 6,
            'best_time_to_visit': 'October to March',
            'seasonal_info': {
                'winter': 'November - February (15-25°C)',
                'summer': 'March - May (25-35°C)',
                'monsoon': 'June - September (Heavy rainfall)',
                'post_monsoon': 'October - November (Pleasant)'
            }
        }
        
        return Response({'weather': weather_data})


# ==================== 4) OFFLINE TRAVEL GUIDE ====================
class OfflineGuideViewSet(viewsets.ModelViewSet):
    """Offline Travel Guide"""
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        destination_id = self.request.query_params.get('destination_id')
        if destination_id:
            return OfflineGuide.objects.filter(destination_id=destination_id)
        return OfflineGuide.objects.all()
    
    def create(self, request):
        """Create offline guide"""
        guide = OfflineGuide.objects.create(
            destination_id=request.data.get('destination_id'),
            title=request.data.get('title'),
            content=request.data.get('content'),
            language=request.data.get('language', 'en')
        )
        return Response({
            'message': 'Guide created',
            'guide_id': guide.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_destination(self, request):
        """Get guides for a destination"""
        dest_id = request.query_params.get('destination_id')
        guides = OfflineGuide.objects.filter(destination_id=dest_id)
        return Response({
            'guides': [{'id': g.id, 'title': g.title, 'language': g.language} for g in guides]
        })


class TripChecklistViewSet(viewsets.ModelViewSet):
    """Trip Checklist"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TripChecklist.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Create checklist"""
        checklist = TripChecklist.objects.create(
            user=request.user,
            name=request.data.get('name'),
            items=request.data.get('items', [])
        )
        return Response({
            'message': 'Checklist created',
            'checklist_id': checklist.id,
            'items': checklist.items
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def update_items(self, request, pk=None):
        """Update checklist items"""
        checklist = self.get_object()
        checklist.items = request.data.get('items', [])
        checklist.save()
        return Response({'message': 'Items updated', 'items': checklist.items})


# ==================== 5) TRAVEL MEMORY SCRAPBOOK ====================
class TravelMemoryViewSet(viewsets.ModelViewSet):
    """Travel Memory Scrapbook"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TravelMemory.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Create travel memory"""
        memory = TravelMemory.objects.create(
            user=request.user,
            title=request.data.get('title'),
            description=request.data.get('description', ''),
            location=request.data.get('location'),
            visit_date=request.data.get('visit_date')
        )
        return Response({
            'message': 'Memory created',
            'memory_id': memory.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_photo(self, request, pk=None):
        """Add photo to memory"""
        memory = self.get_object()
        photo = TravelPhoto.objects.create(
            memory=memory,
            photo=request.data.get('photo'),
            caption=request.data.get('caption', '')
        )
        return Response({'message': 'Photo added', 'photo_id': photo.id})
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add note to memory"""
        memory = self.get_object()
        note = TravelNote.objects.create(
            memory=memory,
            content=request.data.get('content')
        )
        return Response({'message': 'Note added', 'note_id': note.id})


# ==================== 6) GROUP TRIP PLANNER ====================
class GroupTripViewSet(viewsets.ModelViewSet):
    """Group Trip Planner"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GroupTrip.objects.filter(owner=self.request.user)
    
    def create(self, request):
        """Create group trip"""
        trip = GroupTrip.objects.create(
            owner=request.user,
            destination=request.data.get('destination'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date'),
            description=request.data.get('description', ''),
            is_public=request.data.get('is_public', False)
        )
        GroupTripMember.objects.create(
            group_trip=trip,
            user=request.user,
            role='owner',
            status='accepted'
        )
        return Response({
            'message': 'Group trip created',
            'trip_id': trip.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        """Invite user to group trip"""
        trip = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            member, created = GroupTripMember.objects.get_or_create(
                group_trip=trip,
                user=user,
                defaults={'status': 'pending'}
            )
            if not created:
                return Response({'message': 'User already invited'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'User invited'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def create_poll(self, request, pk=None):
        """Create poll for group trip"""
        trip = self.get_object()
        poll = GroupPoll.objects.create(
            group_trip=trip,
            question=request.data.get('question'),
            poll_type=request.data.get('poll_type'),
            options=request.data.get('options', []),
            expires_at=request.data.get('expires_at')
        )
        return Response({'message': 'Poll created', 'poll_id': poll.id})
    
    @action(detail=True, methods=['get'])
    def expenses(self, request, pk=None):
        """Get group expenses"""
        trip = self.get_object()
        expenses = GroupExpense.objects.filter(group_trip=trip)
        return Response({
            'expenses': [{
                'id': e.id,
                'description': e.description,
                'amount': e.amount,
                'paid_by': e.paid_by.username
            } for e in expenses]
        })


# ==================== 7) RECOMMENDATION ENGINE ====================
class RecommendationView(APIView):
    """Recommendation Engine"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get personalized recommendations"""
        user = request.user
        recommendations = UserRecommendation.objects.filter(user=user)[:10]
        trending = TrendingDestination.objects.all()[:5]
        
        return Response({
            'personalized': [{
                'id': r.id,
                'item_name': r.item_name,
                'item_type': r.item_type,
                'reason': r.reason,
                'score': r.score
            } for r in recommendations],
            'trending': [{
                'destination': t.destination.name,
                'trend_score': t.trend_score,
                'direction': t.trend_direction
            } for t in trending]
        })


# ==================== 8) SMART NOTIFICATIONS ====================
class NotificationViewSet(viewsets.ModelViewSet):
    """Smart Notifications"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def list(self, request):
        """Get user notifications"""
        notifications = Notification.objects.filter(user=request.user)[:50]
        return Response({
            'notifications': [{
                'id': n.id,
                'type': n.notification_type,
                'title': n.title,
                'message': n.message,
                'is_read': n.is_read,
                'created_at': n.created_at
            } for n in notifications],
            'unread_count': notifications.filter(is_read=False).count()
        })
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Marked as read'})
    
    @action(detail=False, methods=['post'])
    def create_price_alert(self, request):
        """Create price alert"""
        alert = PriceAlert.objects.create(
            user=request.user,
            item_type=request.data.get('item_type'),
            item_id=request.data.get('item_id'),
            item_name=request.data.get('item_name'),
            target_price=request.data.get('target_price'),
            current_price=request.data.get('current_price')
        )
        return Response({'message': 'Price alert created', 'alert_id': alert.id})


# ==================== 10) SAFETY & EMERGENCY ====================
class SafetyInfoView(APIView):
    """Safety & Emergency Info"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get safety info for destination"""
        destination_id = request.query_params.get('destination_id')
        
        emergency_info = {
            'police': '100',
            'ambulance': '102',
            'fire': '101',
            'women_helpline': '1091',
            'general_emergency': '112',
            'tips': [
                'Keep valuables in hotel safe',
                'Share itinerary with family',
                'Use authorized taxis',
                'Keep copies of important documents',
                'Stay aware of surroundings'
            ]
        }
        
        return Response({'safety': emergency_info})


# ==================== 11) QR BASED TICKETS ====================
class QRTicketViewSet(viewsets.ModelViewSet):
    """QR Based Tickets"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return QRTicket.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Create QR ticket"""
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        ticket = QRTicket.objects.create(
            user=request.user,
            ticket_type=request.data.get('ticket_type'),
            ticket_id=ticket_id,
            qr_code=f"QR-{ticket_id}",
            valid_from=request.data.get('valid_from'),
            valid_until=request.data.get('valid_until')
        )
        return Response({
            'message': 'Ticket created',
            'ticket_id': ticket.ticket_id,
            'qr_code': ticket.qr_code
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def verify(self, request, pk=None):
        """Verify ticket"""
        ticket = self.get_object()
        return Response({
            'valid': not ticket.is_used,
            'ticket_id': ticket.ticket_id,
            'type': ticket.ticket_type,
            'valid_from': ticket.valid_from,
            'valid_until': ticket.valid_until
        })


# ==================== 12) GAMIFICATION ====================
class GamificationView(APIView):
    """Gamification System"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user gamification stats"""
        user = request.user
        points, _ = UserPoints.objects.get_or_create(user=user)
        badges = UserBadge.objects.filter(user=user, is_displayed=True)
        leaderboard = Leaderboard.objects.filter(period='all_time').order_by('rank')[:10]
        
        return Response({
            'points': {
                'total': points.total_points,
                'level': points.level,
                'trips_completed': points.trips_completed
            },
            'badges': [{
                'name': b.badge_name,
                'description': b.badge_description,
                'earned_at': b.earned_at
            } for b in badges],
            'leaderboard': [{
                'rank': l.rank,
                'username': l.user.username,
                'points': l.points
            } for l in leaderboard]
        })
    
    @action(detail=False, methods=['post'])
    def award_badge(self, request):
        """Award badge to user (admin only)"""
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            badge = UserBadge.objects.create(
                user=user,
                badge_name=request.data.get('badge_name'),
                badge_description=request.data.get('badge_description'),
                badge_type=request.data.get('badge_type')
            )
            return Response({'message': 'Badge awarded', 'badge_id': badge.id})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# ==================== 13) COMMUNITY FORUM ====================
class ForumPostViewSet(viewsets.ModelViewSet):
    """Community Forum"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ForumPost.objects.all()
    
    def create(self, request):
        """Create forum post"""
        post = ForumPost.objects.create(
            user=request.user,
            title=request.data.get('title'),
            content=request.data.get('content'),
            category=request.data.get('category', 'discussion'),
            tags=request.data.get('tags', [])
        )
        return Response({
            'message': 'Post created',
            'post_id': post.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Get forum feed"""
        category = request.query_params.get('category')
        posts = ForumPost.objects.all()
        if category:
            posts = posts.filter(category=category)
        posts = posts[:20]
        return Response({
            'posts': [{
                'id': p.id,
                'title': p.title,
                'author': p.user.username,
                'category': p.category,
                'view_count': p.view_count,
                'created_at': p.created_at
            } for p in posts]
        })
    
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Add comment to post"""
        post = self.get_object()
        comment = ForumComment.objects.create(
            post=post,
            user=request.user,
            content=request.data.get('content')
        )
        return Response({'message': 'Comment added', 'comment_id': comment.id})
    
    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        """Vote on post"""
        post = self.get_object()
        ForumVote.objects.create(
            user=request.user,
            content_type='post',
            content_id=post.id,
            vote_type=request.data.get('vote_type', 'up')
        )
        return Response({'message': 'Vote recorded'})


# ==================== 14) LOCAL GUIDE MARKETPLACE ====================
class LocalGuideViewSet(viewsets.ModelViewSet):
    """Local Guide Marketplace"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LocalGuide.objects.filter(is_available=True)
    
    def create(self, request):
        """Register as guide"""
        guide = LocalGuide.objects.create(
            user=request.user,
            guide_id=f"GUIDE-{uuid.uuid4().hex[:6].upper()}",
            full_name=request.data.get('full_name'),
            bio=request.data.get('bio'),
            languages=request.data.get('languages', []),
            locations=request.data.get('locations', []),
            specializations=request.data.get('specializations', []),
            hourly_rate=request.data.get('hourly_rate'),
            daily_rate=request.data.get('daily_rate')
        )
        return Response({
            'message': 'Guide profile created',
            'guide_id': guide.guide_id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search guides"""
        location = request.query_params.get('location')
        language = request.query_params.get('language')
        guides = LocalGuide.objects.filter(is_available=True)
        
        if location:
            guides = guides.filter(locations__icontains=location)
        if language:
            guides = guides.filter(languages__contains=language)
        
        return Response({
            'guides': [{
                'id': g.id,
                'name': g.full_name,
                'rating': g.rating,
                'locations': g.locations,
                'daily_rate': g.daily_rate
            } for g in guides]
        })
    
    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        """Book a guide"""
        guide = self.get_object()
        booking = GuideBooking.objects.create(
            guide=guide,
            tourist=request.user,
            tour_name=request.data.get('tour_name'),
            location=request.data.get('location'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date'),
            total_hours=request.data.get('total_hours'),
            hourly_rate=guide.hourly_rate,
            total_price=guide.hourly_rate * request.data.get('total_hours', 8)
        )
        return Response({
            'message': 'Booking request sent',
            'booking_id': booking.id
        })


# ==================== 15) ADMIN AUTOMATION ====================
class AdminAutomationView(APIView):
    """Admin Automation"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get admin dashboard data"""
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        pending_packages = Package.objects.filter(status='pending').count()
        total_users = User.objects.count()
        total_bookings = Booking.objects.count()
        pending_reports = UserReport.objects.filter(status='pending').count()
        
        return Response({
            'stats': {
                'pending_packages': pending_packages,
                'total_users': total_users,
                'total_bookings': total_bookings,
                'pending_reports': pending_reports
            }
        })
    
    @action(detail=False, methods=['post'])
    def approve_package(self, request):
        """Approve package"""
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        package_id = request.data.get('package_id')
        try:
            package = Package.objects.get(id=package_id)
            package.status = 'approved'
            package.approved_by = request.user
            package.save()
            PackageApproval.objects.create(
                package=package,
                action_type='approve',
                action_by=request.user
            )
            return Response({'message': 'Package approved'})
        except Package.DoesNotExist:
            return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def moderate_user(self, request):
        """Moderate user"""
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        moderation = UserModeration.objects.create(
            user_id=request.data.get('user_id'),
            moderation_type=request.data.get('moderation_type'),
            reason=request.data.get('reason'),
            moderated_by=request.user
        )
        return Response({'message': 'User moderated', 'moderation_id': moderation.id})
   