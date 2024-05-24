from django.urls import path
from .views import SignupView, CsrfTokenView

app_name = 'accounts'
urlpatterns = [
  path('signup/', SignupView.as_view(), name='signup'),
  path('csrf/', CsrfTokenView.as_view(), name='csrf'),
]