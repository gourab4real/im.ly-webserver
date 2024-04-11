from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from UrlShortenerApp.models import UrlShortener

class UrlShortenerSerializer(serializers.ModelSerializer):
    name = ReadOnlyField(source='urlName')
    originalUrl = ReadOnlyField(source='fullUrl')
    
    class Meta:
        model = UrlShortener
        fields = ['name', 'originalUrl']
        depth = 2