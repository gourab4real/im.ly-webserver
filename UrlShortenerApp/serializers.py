from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from UrlShortenerApp.models import UrlShortener

class UrlShortenerSerializer(serializers.ModelSerializer):
    name = ReadOnlyField(source='urlName')
    originalUrl = ReadOnlyField(source='fullUrl')
    shortenedUrl = serializers.SerializerMethodField()
    
    class Meta:
        model = UrlShortener
        fields = ['name', 'originalUrl', 'shortenedUrl']
        depth = 2

    def get_shortenedUrl(self, instance):
        baseUrl = self.context['request'].build_absolute_uri('/')
        return baseUrl+instance.shortenedUrl