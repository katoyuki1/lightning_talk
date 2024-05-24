from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

class CsrfTokenView(View):
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(csrf_exempt)  # 追加: このビューをCSRF検証から免除
    def get(self, request, *args, **kwargs):
        response = JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE', '')})
        response["Access-Control-Allow-Origin"] = "http://localhost:5174"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

class SignupView(CreateView):
  form_class = SignupForm
  success_url = reverse_lazy('index')
  # template_name = 'registration/signup.html'

  def form_valid(self, form):
    valid = super().form_valid(form)
    login(self.request, self.object)
    return valid