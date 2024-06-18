from rest_framework import serializers
from .models import Audio, Advice

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'user', 'title', 'description', 'voice', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']  # 'user' を read_only に設定

class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = ['id', 'audio', 'user', 'advice_text', 'created_at']
        read_only_fields = ['audio', 'user', 'created_at']