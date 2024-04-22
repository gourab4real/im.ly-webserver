from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from UrlShortenerApp.models import URL, UrlShortener
from UrlShortenerApp.randomGen import IDGenerator
from UrlShortenerApp.serializers import URLSerializer, UrlShortenerSerializer


class UrlViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    @action(detail=False, methods=['post'])
    def addUrl(self, request):
        urlName = request.data.get('urlName')
        fullUrl = request.data.get('fullUrl')

        val = URLValidator()
        try:
            val(fullUrl)
            urlObj, created = URL.objects.get_or_create(fullUrl=fullUrl)

            if created:
                urlObj.urlName = urlName
                urlObj.save()

                return Response({'status': 1, 'msg': 'Url added successfully'}, status=status.HTTP_201_CREATED)
            return Response({'status': 2, 'msg': 'Url already exists'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'status': -2, 'msg': f'Invalid website: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': -1, 'msg': f'Something went wrong ({ex})'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def getUrlList(self, request):
        try:
            urlList = URL.objects.all()
            urlListSerialized = self.serializer_class(urlList, many=True)

            return Response({'status': 1, 'urlList': urlListSerialized.data}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': -1, 'msg': f'Something went wrong ({ex})'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def getUrlById(self, request):
        urlId = request.data.get('urlId')

        try:
            urlObj = URL.objects.get(id=urlId)
            urlObjSerialized = self.serializer_class(urlObj)

            return Response({'status': 1, 'urlDetails': urlObjSerialized.data}, status=status.HTTP_200_OK)
        except URL.DoesNotExist as ex:
            return Response({'status': -1, 'msg': "URL does not exists", 'err': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': -2, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def getUrlByFullUrl(self, request):
        fullUrl = request.data.get('fullUrl')

        try:
            urlObj = URL.objects.get(fullUrl=fullUrl)
            urlObjSerialized = self.serializer_class(urlObj)

            return Response({'status': 1, 'urlDetails': urlObjSerialized.data}, status=status.HTTP_200_OK)
        except URL.DoesNotExist as ex:
            return Response({'status': -1, 'msg': "URL does not exists", 'err': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': -2, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UrlShortenerView(viewsets.ModelViewSet):
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
        
    @action(detail=False, methods=['post'])
    def shortenUrl(self, request):
        urlId = request.data.get('urlId')

        try:
            url_obj = URL.objects.get(id=urlId)

            shortened_url_name = f"{url_obj.urlName}-Shortened"
            shortened_url_obj, created = UrlShortener.objects.get_or_create(shortenedUrlName=shortened_url_name)

            if created:
                short_url = IDGenerator(8).generate_id()
                shortened_url_obj.url = url_obj
                shortened_url_obj.shortenedUrl = short_url
                shortened_url_obj.save()
                status_code = status.HTTP_201_CREATED
                msg = "shortened url created"
            else:
                short_url = shortened_url_obj.shortenedUrl
                status_code = status.HTTP_200_OK
                msg = "shortened url already exists"

            serialized_data = self.serializer_class(shortened_url_obj, context={'request': request}).data

            return Response({'status': 1 if created else 2, 'msg': msg, 'originalInput': serialized_data}, status=status_code)
        except URL.DoesNotExist as ex:
            return Response({'status': -2, 'msg': "URL does not exists", 'err': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': -1, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['get'])
    def redirect_original_url(request, short_url):
        # Look up the original URL in the database based on the short URL
        url_object = get_object_or_404(UrlShortener, shortenedUrl=short_url)
    
        # Perform the redirection
        return redirect(url_object.url.fullUrl)
    
    @action(detail=False, methods=['get'])
    def getAllShortenedUrl(self, request):
        try:
            urlObj = UrlShortener.objects.all()
            urlObjSerialized = self.serializer_class(urlObj, many=True, context={'request': request})

            return Response({'status': 1, 'originalInput': urlObjSerialized.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': -1, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def getShortenedUrlById(self, request):
        shortenedUrlId = request.data.get('shortenedUrlId')

        try:
            urlShortenerObj = UrlShortener.objects.get(id=shortenedUrlId)
            urlShortenerObjSerialized = self.serializer_class(urlShortenerObj, context={'request': request})

            return Response({'status': 1, 'shortenedUrlDetails': urlShortenerObjSerialized.data}, status=status.HTTP_200_OK)
        except UrlShortener.DoesNotExist as ex:
            return Response({'status': -1, 'msg': "URL does not exists", 'err': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': -2, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def getShortenedUrlByFullUrl(self, request):
        fullUrl = request.data.get('fullUrl')

        try:
            urlObj = URL.objects.get(fullUrl=fullUrl)
            urlShortenerObj = UrlShortener.objects.get(url=urlObj)
            urlShortenerObjSerialized = self.serializer_class(urlShortenerObj, context={'request': request})

            return Response({'status': 1, 'shortenedUrlDetails': urlShortenerObjSerialized.data}, status=status.HTTP_200_OK)
        except UrlShortener.DoesNotExist as ex:
            return Response({'status': -1, 'msg': "URL does not exists", 'err': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': -2, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)