from django.urls import path, include
from rest_framework import routers

from UrlShortenerApp.views import UrlShortenerView, UrlViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register('url', UrlViewSet)
router.register('shortenUrl', UrlShortenerView)

urlpatterns = [
    path('api/', include(router.urls)),
]