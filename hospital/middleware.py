from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    EXEMPT_URLS = [
        reverse('login'),
        reverse('register'),
        '/accounts/',  # Django auth URLs
        '/static/',
        '/media/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip if already authenticated or accessing exempt URLs
        if request.user.is_authenticated or any(request.path.startswith(url) for url in self.EXEMPT_URLS):
            return None
            
        # Redirect to login page for protected pages
        login_url = reverse(settings.LOGIN_URL)
        return HttpResponseRedirect(f"{login_url}?next={request.path}")
