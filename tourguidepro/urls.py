from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

from api.views import home, book_hotel


# Language switch url
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# API URLs - NOT under i18n to avoid language prefixes
urlpatterns += [
    path('api/', include('api.urls')),
]

# Main urls with i18n support - for pages only
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),

    path('', home, name='home'),
    path('home/', home, name='home-alt'),
    re_path(r'^Home\.html?/?$', home),
    re_path(r'^home\.html?/?$', home),

    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),

    path('destination/', TemplateView.as_view(template_name='destination.html'), name='destination'),

    path('hotel/', TemplateView.as_view(template_name='hotel.html'), name='hotel'),

    path('book-hotel/', book_hotel, name='book_hotel'),

    path('cab/', TemplateView.as_view(template_name='cab.html'), name='cab'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),

    path('itinerary/', TemplateView.as_view(template_name='iterenary.html'), name='itinerary'),
    path('features/', TemplateView.as_view(template_name='features.html'), name='features'),
    
    # User dropdown routes
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('history/', TemplateView.as_view(template_name='history.html'), name='history'),
    path('wishlist/', TemplateView.as_view(template_name='wishlist.html'), name='wishlist'),
    path('payments/', TemplateView.as_view(template_name='payments.html'), name='payments'),
    path('gallery/', TemplateView.as_view(template_name='gallery.html'), name='gallery'),
    path('reviews/', TemplateView.as_view(template_name='reviews.html'), name='reviews'),
    path('notifications/', TemplateView.as_view(template_name='notifications.html'), name='notifications'),
    path('settings/', TemplateView.as_view(template_name='settings.html'), name='settings'),
    path('help/', TemplateView.as_view(template_name='help.html'), name='help'),
)


# Static & Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
