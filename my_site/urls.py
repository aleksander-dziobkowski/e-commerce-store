from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,)
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from drf_spectacular.utils import extend_schema
from reviews.views import MyTokenObtainPairView

TokenObtainPairView = extend_schema(tags=['Authentication'])(TokenObtainPairView)
TokenRefreshView = extend_schema(tags=['Authentication'])(TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('portfolio.urls')),
    path('store/',include("store.urls")),
    path("store/accounts/", include("allauth.urls")),
    path("reviews-api/",include("reviews.urls")),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
