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


# Main urls with i18n support
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),

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
)


# Static & Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
