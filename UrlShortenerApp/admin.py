from django.contrib import admin

from UrlShortenerApp.models import UrlShortener

class UrlShortenerAdmin(admin.ModelAdmin):
    list_display = ['urlName', 'shortenedUrl',]
    search_fields = ['urlName',]

admin.site.register(UrlShortener, UrlShortenerAdmin)