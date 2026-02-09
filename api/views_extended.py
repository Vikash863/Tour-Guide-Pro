from datetime import datetime, timedelta
from decimal import Decimal
import math
import random
import string

from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Destination, Hotel, Cab, Booking, Contact,
    GPSLocation, TripTrack, FavoriteLocation,
    Expense, ExpenseCategory, ExpenseBudget,
    TravelChecklist, ChecklistItem, ChecklistTemplate,
    ReferralCode, Referral, WeatherCache,
    TripPlan
)


# ==================== GPS MAP TRACKING VIEWS ====================
class GPSLocationViewSet(viewsets.ModelViewSet):
    serializer_class = None  # Placeholder
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GPSLocation.objects.filter(user=self.request.user)


class TripTrackViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TripTrack.objects.filter(user=self.request.user)


class FavoriteLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteLocation.objects.filter(user=self.request.user)


# ==================== EXPENSE TRACKER VIEWS ====================
class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return ExpenseCategory.objects.all()


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseBudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ExpenseBudget.objects.filter(user=self.request.user)


# ==================== TRAVEL CHECKLIST VIEWS ====================
class TravelChecklistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TravelChecklist.objects.filter(user=self.request.user)


class ChecklistItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        checklist_id = self.kwargs.get('checklist_id')
        return ChecklistItem.objects.filter(checklist_id=checklist_id)


# ==================== REFERRAL SYSTEM VIEWS ====================
class ReferralCodeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ReferralCode.objects.filter(user=self.request.user)


class ReferralViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Referral.objects.filter(
                Q(referrer=self.request.user) | Q(referred=self.request.user)
            )
        return Referral.objects.none()


# ==================== WEATHER API VIEWS ====================
@api_view(['GET'])
@permission_classes([AllowAny])
def weather_info(request):
    city = request.query_params.get('city')
    destination_id = request.query_params.get('destination_id')
    
    if destination_id:
        destination = Destination.objects.filter(id=destination_id).first()
        if destination:
            city = destination.city
    
    if not city:
        return Response({'error': 'City parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to get cached weather
    cached = WeatherCache.objects.filter(city__icontains=city).order_by('-cached_at').first()
    if cached and (timezone.now() - cached.cached_at) < timedelta(hours=1):
        return Response({
            'city': cached.city,
            'country': cached.country,
            'temperature': cached.temperature,
            'humidity': cached.humidity,
            'description': cached.description,
            'icon': cached.icon,
            'wind_speed': cached.wind_speed
        })
    
    # Mock weather data (integrate with OpenWeatherMap API in production)
    weather_data = {
        'city': city,
        'country': 'India',
        'temperature': 25 + random.randint(-5, 10),
        'humidity': random.randint(40, 80),
        'description': ['Sunny', 'Partly Cloudy', 'Clear', 'Light Rain'][random.randint(0, 3)],
        'icon': ['01d', '02d', '03d', '10d'][random.randint(0, 3)],
        'wind_speed': random.randint(5, 25),
        'forecast_date': timezone.now().date().isoformat()
    }
    
    # Cache the weather data
    WeatherCache.objects.create(**weather_data)
    
    return Response(weather_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def forecast(request):
    """Get weather forecast for destination"""
    city = request.query_params.get('city')
    days = int(request.query_params.get('days', 7))
    
    if not city:
        return Response({'error': 'City parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    forecast_data = []
    for i in range(days):
        date = timezone.now().date() + timedelta(days=i)
        forecast_data.append({
            'date': date.isoformat(),
            'temperature': 22 + random.randint(-8, 12),
            'humidity': random.randint(40, 85),
            'description': ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy'][random.randint(0, 3)],
            'icon': ['01d', '02d', '03d', '10d'][random.randint(0, 3)]
        })
    
    return Response({
        'city': city,
        'forecast': forecast_data
    })


# ==================== PAGE VIEWS ====================
def expense_tracker(request):
    return render(request, 'expense_tracker.html')


def checklist_view(request):
    return render(request, 'checklist.html')


def referral_view(request):
    return render(request, 'referral.html')


def map_tracking_view(request):
    return render(request, 'map_tracking.html')


def weather_view(request):
    return render(request, 'weather.html')
