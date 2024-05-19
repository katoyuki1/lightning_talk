from rest_framework import viewsets # DRFからviewsetsをインポート。ウェブページの表示やデータ処理などの一連の操作をひとまとめにしたクラス（=ビューセット）
from .models import Video 
from .serializers import VideoSerializer 

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer