from django.urls import path, include
from rest_framework import routers

from UrlShortenerApp.views import UrlShortenerView

router = routers.DefaultRouter(trailing_slash=False)

router.register('shortenUrl', UrlShortenerView)

urlpatterns = [
    path('api/', include(router.urls)),
]