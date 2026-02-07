"""
URL configuration for tourguidepro project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# 🔹 IMPORT MongoDB-powered home view
from api.views import home

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # APIs (DRF)
    path('api/', include('api.urls')),

    # =========================
    # Home Page (MongoDB)
    # =========================
    path('', home, name='home'),
    path('home/', home, name='home-alt'),
    re_path(r'^Home\.html?/?$', home),
    re_path(r'^home\.html?/?$', home),

    # =========================
    # Login Page
    # =========================
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    re_path(r'^login\.html?/?$', TemplateView.as_view(template_name='login.html')),

    # =========================
    # Signup Page
    # =========================
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
    re_path(r'^signup\.html?/?$', TemplateView.as_view(template_name='signup.html')),

    # =========================
    # Destination Page
    # =========================
    path('destination/', TemplateView.as_view(template_name='destination.html'), name='destination'),
    re_path(r'^destination\.html?/?$', TemplateView.as_view(template_name='destination.html')),

    # =========================
    # Hotel Page
    # =========================
    path('hotel/', TemplateView.as_view(template_name='hotel.html'), name='hotel'),
    re_path(r'^hotel\.html?/?$', TemplateView.as_view(template_name='hotel.html')),

    # =========================
    # Cab Page
    # =========================
    path('cab/', TemplateView.as_view(template_name='cab.html'), name='cab'),
    re_path(r'^cab\.html?/?$', TemplateView.as_view(template_name='cab.html')),

    # =========================
    # Contact Page
    # =========================
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    re_path(r'^contact\.html?/?$', TemplateView.as_view(template_name='contact.html')),

    # =========================
    # Itinerary Page
    # =========================
    path('itinerary/', TemplateView.as_view(template_name='iterenary.html'), name='itinerary'),
    re_path(r'^itinerary\.html?/?$', TemplateView.as_view(template_name='iterenary.html')),
    re_path(r'^iterenary\.html?/?$', TemplateView.as_view(template_name='iterenary.html')),
]

# Static & Media (Development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
