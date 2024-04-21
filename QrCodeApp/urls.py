from django.urls import path, include
from rest_framework import routers

from QrCodeApp.views import QrCodeHandler

router = routers.DefaultRouter(trailing_slash=False)

router.register('qrCodeUrl', QrCodeHandler)

urlpatterns = [
    path('api/', include(router.urls))
]
