from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioViewSet

router = DefaultRouter()
router.register(r'', AudioViewSet)  # 'r'audio' から 'r'' に変更

urlpatterns = [
    path('', include(router.urls)),  # ルータのURLをインクルード
]