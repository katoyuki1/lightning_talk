import os
import django
from django.core.mail import send_mail

# Django設定モジュールを設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Djangoを初期化
django.setup
send_mail(
    'Test Subject',
    'Test message.',
    '0me3210g039530z@gmail.com@gmail.com',
    ['yuki-kato@yk-engineer.net'],
    fail_silently=False,
)