from django.db import models
from django.contrib.auth.models import User

class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーと関連付け
    title = models.CharField(max_length=255)
    description = models.TextField()
    voice = models.FileField(upload_to='voices/')  # 音声ファイルの保存先
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Advice(models.Model):
    audio = models.ForeignKey(Audio, related_name='advices', on_delete=models.CASCADE)  # 音声ファイルと関連付け
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 提案したユーザーと関連付け
    advice_text = models.TextField()  # 改善案のテキスト
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Advice for {self.audio.title}"