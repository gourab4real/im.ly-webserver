from rest_framework import serializers

from QrCodeApp.models import UrlQrCode

class UrlQrCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UrlQrCode
        fields = '__all__'
        depth = 2
