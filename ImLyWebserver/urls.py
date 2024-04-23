from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from UrlShortenerApp.views import UrlShortenerView
from UserApp.views import CreateUserView, LogoutView

schema_view = get_schema_view(
    openapi.Info(
        title="im.ly API",
        default_version='v1',
        description="Tryout im.ly API",
        # terms_of_service="https://www.example.com/terms/",
        # contact=openapi.Contact(email="contact@example.com"),
        # license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'api/token/', TokenObtainPairView.as_view(), name="access_token"),
    path(r'api/token/refresh', TokenRefreshView.as_view(), name="refresh_token"),
    path(r'api-auth/', include("rest_framework.urls")),
    path(r'api/user/register/', CreateUserView.as_view(), name="register"),
    path(r'api/logout/', LogoutView.as_view()),

    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path(r'urlshortenerapp/', include('UrlShortenerApp.urls')),
    path(r'<str:short_url>', UrlShortenerView.redirect_original_url),
    path(r'qrcodeapp/', include('QrCodeApp.urls')),
]
