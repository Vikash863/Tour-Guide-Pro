"""
Extended URL patterns for Tour Guide Pro - All 15 Features
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_extended import (
    TripPlanViewSet, TripPreferenceViewSet, BudgetTrackerViewSet,
    NearbyPlacesViewSet, OfflineGuideViewSet, TripChecklistViewSet,
    TravelMemoryViewSet, GroupTripViewSet, NotificationViewSet,
    QRTicketViewSet, ForumPostViewSet, LocalGuideViewSet,
    CurrencyConverterView, WeatherView, RecommendationView,
    SafetyInfoView, GamificationView, AdminAutomationView
)

router = DefaultRouter()

# 1) Smart Trip Assistant (AI)
router.register(r'trip-plans', TripPlanViewSet, basename='trip-plans')
router.register(r'trip-preferences', TripPreferenceViewSet, basename='trip-preferences')

# 2) Budget Calculator
router.register(r'budget-trackers', BudgetTrackerViewSet, basename='budget-trackers')

# 3) Nearby Places Finder
router.register(r'nearby-places', NearbyPlacesViewSet, basename='nearby-places')

# 4) Offline Travel Guide
router.register(r'offline-guides', OfflineGuideViewSet, basename='offline-guides')
router.register(r'trip-checklists', TripChecklistViewSet, basename='trip-checklists')

# 5) Travel Memory Scrapbook
router.register(r'travel-memories', TravelMemoryViewSet, basename='travel-memories')

# 6) Group Trip Planner
router.register(r'group-trips', GroupTripViewSet, basename='group-trips')

# 8) Smart Notifications
router.register(r'notifications', NotificationViewSet, basename='notifications')

# 11) QR Based Tickets
router.register(r'qr-tickets', QRTicketViewSet, basename='qr-tickets')

# 13) Community Forum
router.register(r'forum-posts', ForumPostViewSet, basename='forum-posts')

# 14) Local Guide Marketplace
router.register(r'local-guides', LocalGuideViewSet, basename='local-guides')

urlpatterns = [
    # Currency Converter
    path('currency/convert/', CurrencyConverterView.as_view(), name='currency-converter'),
    path('currency/currencies/', CurrencyConverterView.as_view(), name='currencies'),
    
    # Weather
    path('weather/', WeatherView.as_view(), name='weather'),
    
    # Recommendations
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    
    # Safety & Emergency
    path('safety/', SafetyInfoView.as_view(), name='safety'),
    
    # Gamification
    path('gamification/', GamificationView.as_view(), name='gamification'),
    
    # Admin Automation
    path('admin/dashboard/', AdminAutomationView.as_view(), name='admin-dashboard'),
    path('admin/approve-package/', AdminAutomationView.as_view(), name='approve-package'),
    path('admin/moderate-user/', AdminAutomationView.as_view(), name='moderate-user'),
    
    # Include router URLs
    path('', include(router.urls)),
]
