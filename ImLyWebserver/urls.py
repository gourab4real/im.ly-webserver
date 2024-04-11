from django.contrib import admin
from django.urls import path, include

from UrlShortenerApp.views import UrlShortenerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'urlshortenerapp/', include('UrlShortenerApp.urls')),
    path(r'<str:short_url>', UrlShortenerView.redirect_original_url)
]
