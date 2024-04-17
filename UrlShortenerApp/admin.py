from django.contrib import admin

from UrlShortenerApp.models import URL, UrlQrCode, UrlShortener

class URLAdmin(admin.ModelAdmin):
    list_display = ['urlName', 'fullUrl',]
    search_fields = ['urlName',]

admin.site.register(URL, URLAdmin)

class UrlShortenerAdmin(admin.ModelAdmin):
    list_display = ['url', 'shortenedUrlName', 'shortenedUrl',]
    search_fields = ['url__urlName', 'shortenedUrlName']

admin.site.register(UrlShortener, UrlShortenerAdmin)

class UrlQrCodeAdmin(admin.ModelAdmin):
    list_display = ['qrCodeName', 'url',]
    search_fields = ['qrCodeName',]

admin.site.register(UrlQrCode, UrlQrCodeAdmin)