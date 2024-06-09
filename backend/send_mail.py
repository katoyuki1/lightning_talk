import os
import django
from django.core.mail import send_mail
from decouple import config  # .envファイルから設定を読み込むためのパッケージ

# Django設定モジュールを設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Djangoを初期化
django.setup
send_mail(
    'Test Subject',
    'Test message.',
    config('EMAIL_HOST_USER'),  # 送信元のメールアドレス
    [config('EMAIL_SEND_TEST_USER')], #　送信先メールアドレス
    fail_silently=False,
)