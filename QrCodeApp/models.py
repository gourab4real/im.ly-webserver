from django.db import models

from UrlShortenerApp.models import URL

class UrlQrCode(models.Model):
    url = models.ForeignKey(URL, null=True, blank=True, on_delete=models.DO_NOTHING)
    qrCodeName = models.CharField(max_length=255)
    qrCode = models.TextField(null=True, blank=True)
    dateUploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.url.urlName) + " --- " + str(self.qrCodeName)