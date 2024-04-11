from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response

from UrlShortenerApp.models import UrlShortener
from UrlShortenerApp.randomGen import IDGenerator
from UrlShortenerApp.serializers import UrlShortenerSerializer

class UrlShortenerView(viewsets.ModelViewSet):
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
        
    @action(detail=False, methods=['post'])
    def shortenUrl(self, request):
        urlName = request.data.get('urlName')
        fullUrl = request.data.get('fullUrl')

        base_url = request.build_absolute_uri('/')

        try:
            urlObj, created = UrlShortener.objects.get_or_create(fullUrl=fullUrl)

            if created:
                idgen = IDGenerator(8)
                shortUrl = str(idgen.generate_id())
                shortUrlDisplay = base_url + shortUrl

                urlObj.urlName = urlName
                urlObj.shortenedUrl = shortUrl

                urlObj.save()

                urlObjSerialized = self.serializer_class(urlObj)

                return Response({'status': 1, 'msg': "shortened url created", 'originalInput': urlObjSerialized.data, 'shortenedUrl': shortUrlDisplay}, status=status.HTTP_201_CREATED)
            else:
                urlObjSerialized = self.serializer_class(urlObj)

                shortUrl = urlObj.shortenedUrl
                shortUrlDisplay = base_url + shortUrl

                return Response({'status': 2, 'msg': "shortened url already exists", 'originalInput': urlObjSerialized.data, 'shortenedUrl': shortUrlDisplay}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': -1, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['get'])
    def redirect_original_url(request, short_url):
        # Look up the original URL in the database based on the short URL
        url_object = get_object_or_404(UrlShortener, shortenedUrl=short_url)
    
        # Perform the redirection
        return redirect(url_object.fullUrl)
