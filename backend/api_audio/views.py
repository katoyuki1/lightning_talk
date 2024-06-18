from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Audio, Advice
from .serializers import AudioSerializer, AdviceSerializer
import whisper
from openai import OpenAI
import os
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv('../.env')

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
    
    def perform_destroy(self, instance):
        # ファイルの削除などの前処理をここに追加できます
        instance.voice.delete(save=False)  # 音声ファイルを削除
        super().perform_destroy(instance)

    @action(detail=True, methods=['post'])
    def transcribe_and_advice(self, request, pk=None):
        audio = self.get_object()
        audio_path = audio.voice.path

        # Whisperで文字起こし
        model = whisper.load_model("small")
        result = model.transcribe(audio_path)
        transcribed_text = result["text"]

        # OpenAI APIで改善案を取得
        openai_api_key = os.getenv('OPENAI_API_KEY')
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは優秀なエディターです。"},
                {"role": "user", "content": f"以下の文章を改善するには？具体的に提案して:\n\n{transcribed_text}"}
            ],
            temperature=0.7
        )

        # improvement_suggestions = response.choices[0].message['content'].strip()
        improvement_suggestions = response.choices[0].message.content
        print("improvement_suggestions: ", improvement_suggestions)

        # 改善案を保存
        advice = Advice.objects.create(
            audio=audio,
            user=request.user,
            advice_text=improvement_suggestions
        )

        return Response({"transcription": transcribed_text, "advice": improvement_suggestions}, status=status.HTTP_200_OK)