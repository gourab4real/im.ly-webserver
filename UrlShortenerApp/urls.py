from django.urls import path, include
from rest_framework import routers

from UrlShortenerApp.views import QrCodeHandler, UrlShortenerView

router = routers.DefaultRouter(trailing_slash=False)

router.register('shortenUrl', UrlShortenerView)
router.register('qrCodeUrl', QrCodeHandler)

urlpatterns = [
    path('api/', include(router.urls)),
]