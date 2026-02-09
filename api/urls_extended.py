from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views_extended import (
    GPSLocationViewSet, TripTrackViewSet, FavoriteLocationViewSet,
    ExpenseCategoryViewSet, ExpenseViewSet, ExpenseBudgetViewSet,
    TravelChecklistViewSet, ChecklistItemViewSet,
    ReferralCodeViewSet, ReferralViewSet,
    weather_info, forecast,
    expense_tracker, checklist_view, referral_view, map_tracking_view, weather_view
)

# Router for viewsets
router = DefaultRouter()
router.register(r'gps', GPSLocationViewSet, basename='gps')
router.register(r'trips', TripTrackViewSet, basename='trips')
router.register(r'favorites', FavoriteLocationViewSet, basename='favorites')
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expense-categories')
router.register(r'expenses', ExpenseViewSet, basename='expenses')
router.register(r'budgets', ExpenseBudgetViewSet, basename='budgets')
router.register(r'checklists', TravelChecklistViewSet, basename='checklists')
router.register(r'checklist-items', ChecklistItemViewSet, basename='checklist-items')
router.register(r'referral-codes', ReferralCodeViewSet, basename='referral-codes')
router.register(r'referrals', ReferralViewSet, basename='referrals')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Weather endpoints
    path('weather/', weather_info, name='weather-info'),
    path('weather/forecast/', forecast, name='weather-forecast'),
    
    # Page views
    path('expense-tracker/', expense_tracker, name='expense-tracker'),
    path('checklist/', checklist_view, name='checklist'),
    path('referral/', referral_view, name='referral'),
    path('map-tracking/', map_tracking_view, name='map-tracking'),
    path('weather/', weather_view, name='weather'),
]
