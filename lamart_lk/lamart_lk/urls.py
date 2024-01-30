from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = (
    [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

        path('admin/', admin.site.urls),
        path('review/', include('performance_review.urls'), name='performance review'),
        path('auth/', include('authentication.urls'), name='authentication'),
        path('profile/', include('user_profile.urls'), name='profile'),
        path('salary/', include('salary.urls'), name='salary'),
        path('planning/', include('planning.urls'), name='planning')
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)