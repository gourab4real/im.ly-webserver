from django.contrib import admin

from QrCodeApp.models import UrlQrCode

class UrlQrCodeAdmin(admin.ModelAdmin):
    list_display = ['qrCodeName', 'url', 'dateUploaded',]
    search_fields = ['qrCodeName',]

admin.site.register(UrlQrCode, UrlQrCodeAdmin)