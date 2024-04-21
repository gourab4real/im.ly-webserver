from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from UrlShortenerApp.models import URL, UrlShortener

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = '__all__'
        depth = 1

class UrlShortenerSerializer(serializers.ModelSerializer):
    url = URLSerializer()
    shortenedUrlName = ReadOnlyField()
    shortenedUrl = serializers.SerializerMethodField()
    
    class Meta:
        model = UrlShortener
        fields = ['id', 'url', 'shortenedUrlName', 'shortenedUrl']
        depth = 1

    def get_shortenedUrl(self, instance):
        baseUrl = self.context['request'].build_absolute_uri('/')
        return baseUrl+instance.shortenedUrl
    