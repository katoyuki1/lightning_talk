from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Audio
from .serializers import AudioSerializer

class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("Custom create method called")  # デバッグ用メッセージ
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        print("Perform create called")  # デバッグ用メッセージ
        print(f"User: {self.request.user}")  # リクエストのユーザーを確認
        serializer.save(user=self.request.user)