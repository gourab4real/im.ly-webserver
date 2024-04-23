from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from UserApp.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refreshToken = RefreshToken.for_user(user)

            return Response({"refresh": str(refreshToken), "access": str(refreshToken.access_token)}, status=status.HTTP_201_CREATED)
        return Response({"error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refreshToken = request.data('refreshToken')

            token = RefreshToken(refreshToken)
            token.blacklist()

            return Response({"msg": "Successfully logged out"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)