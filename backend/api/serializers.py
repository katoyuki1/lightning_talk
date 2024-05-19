from rest_framework import serializers # Django REST Frameworkのserializersモジュールをインポート
from .models import Video # 同じディレクトリにあるmodels.pyファイルからItemモデルをインポート

class VideoSerializer(serializers.ModelSerializer):
    # ItemSerializerクラスの設定を行う内部クラスMetaを定義
    class Meta:
        # シリアライザが扱うモデルをVideoに指定しています
        model = Video
        # シリアライズされるときに含めるフィールドをid、name、descriptionに限定する
        fields = ['id', 'title', 'description', 'video', 'created_at']