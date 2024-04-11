from django.db import models

class UrlShortener(models.Model):
    urlName = models.CharField(max_length=255, null=True)
    fullUrl = models.TextField()
    shortenedUrl = models.TextField()

    def __str__(self):
        return str(self.urlName) + " --- " + str(self.shortenedUrl)