from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),  # allauth のURLをインクルード
    path('api/audio/', include('api_audio.urls')), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# DEBUGがTrueの場合にのみ、メディアファイルのURLパターンを追加
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
