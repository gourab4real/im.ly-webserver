from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from QrCodeApp.models import UrlQrCode
from QrCodeApp.qrCodeGen import QRCodeGen
from QrCodeApp.serializers import UrlQrCodeSerializer
from UrlShortenerApp.models import URL

class QrCodeHandler(viewsets.ModelViewSet):
    queryset = UrlQrCode.objects.all()
    serializer_class = UrlQrCodeSerializer

    @action(detail=False, methods=['post'])
    def addQrCode(self, request):
        urlId = request.data.get('urlId')
        fullUrl = request.data.get('fullUrl')

        try:
            if urlId and not(fullUrl):
                urlObj = URL.objects.get(id=urlId)
            elif fullUrl and not(urlId):
                urlObj = URL.objects.get(fullUrl=fullUrl)
            elif fullUrl and urlId:
                urlObj = URL.objects.get(id=urlId, fullUrl=fullUrl)
            else:
                return Response({'status': -2, 'msg': 'There is no payload in the body'}, status=status.HTTP_400_BAD_REQUEST)

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
        except URL.DoesNotExist as e:
            return Response({'status': -3, 'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'status': -4, 'msg': f"Something went wrong: {ex}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def getQrCodeList(self, request):
        try:
            qrCodeList = UrlQrCode.objects.all()
            qrCodeListSerialized = self.serializer_class(qrCodeList, many=True)

            return Response({'status': 1, 'qrCodeList': qrCodeListSerialized.data}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': -1, 'msg': f'Something went wrong ({ex})'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def getQrCodeById(self, request):
        qrCodeId = request.data.get('qrCodeId')

        try:
            qrCodeObj = UrlQrCode.objects.get(id=qrCodeId)
            qrCodeObjSerialized = self.serializer_class(qrCodeObj)

            return Response({'status': 1, 'qrCodeDetails': qrCodeObjSerialized.data}, status=status.HTTP_200_OK)
        except UrlQrCode.DoesNotExist as ex:
            return Response({'status': -1, 'msg': "Qr Code does not exists", 'err': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': -2, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def getQrCodeByFullUrl(self, request):
        fullUrl = request.data.get('fullUrl')

        try:
            urlObj = URL.objects.get(fullUrl=fullUrl)
            qrCodeObj = UrlQrCode.objects.get(url=urlObj)
            qrCodeObjSerialized = self.serializer_class(qrCodeObj)

            return Response({'status': 1, 'qrCodeDetails': qrCodeObjSerialized.data}, status=status.HTTP_200_OK)
        except UrlQrCode.DoesNotExist as ex:
            return Response({'status': -1, 'msg': "Qr Code does not exists", 'err': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': -2, 'msg': "Something went wrong", 'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)
