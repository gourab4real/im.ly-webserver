from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response

import qrcode
import qrcode.image.svg
from io import BytesIO
from PIL import Image
import base64

from UrlShortenerApp.models import URL, UrlQrCode, UrlShortener
from UrlShortenerApp.qrCodeGen import QRCodeGen
from UrlShortenerApp.randomGen import IDGenerator
from UrlShortenerApp.serializers import UrlQrCodeSerializer, UrlShortenerSerializer


class UrlShortenerView(viewsets.ModelViewSet):
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
        
    # Inefficient Code, need to re-write
    @action(detail=False, methods=['post'])
    def shortenUrl(self, request):
        url_name = request.data.get('urlName')
        full_url = request.data.get('fullUrl')

        try:
            url_obj, created = URL.objects.get_or_create(fullUrl=full_url)

            if created:
                url_obj.urlName = url_name
                url_obj.save()

            shortened_url_name = f"{url_name}-Shortened"
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


# QRCode Generator
class QrCodeHandler(viewsets.ModelViewSet):
    queryset = UrlQrCode.objects.all()
    serializer_class = UrlQrCodeSerializer

    @action(detail=False, methods=['post'])
    def addQrCode(self, request):
        urlId = request.data.get('urlId')

        urlObj = URL.objects.get(id=urlId)
        url = urlObj.fullUrl
        qrCodeName = urlObj.urlName + "-qrCode"

        img_base64 = QRCodeGen.generate_qr(url)

        obj, created = UrlQrCode.objects.get_or_create(url=urlObj, qrCode=img_base64)

        if created:
            obj.qrCodeName = qrCodeName
            obj.qrCode = img_base64

            obj.save()

            objSerialized = self.serializer_class(obj)

            return Response({'status': 1, 'msg': 'QrCode Generated', 'data': objSerialized.data}, status=status.HTTP_201_CREATED)
        
        objSerialized = self.serializer_class(obj)

        return Response({'status': -1, 'msg': 'QrCode Already Exists', 'data': objSerialized.data}, status=status.HTTP_200_OK)