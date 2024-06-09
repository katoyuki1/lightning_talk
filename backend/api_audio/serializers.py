from rest_framework import serializers
from .models import Audio

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'user', 'title', 'description', 'voice', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']  # 'user' を read_only に設定