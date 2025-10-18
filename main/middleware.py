from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class HTTPSRedirectMiddleware:
    """
    Redirect HTTP requests to HTTPS when behind a proxy (like ngrok) that sets X-Forwarded-Proto.
    
    This prevents Facebook OAuth "insecure page" errors by ensuring users always access
    the app over HTTPS when using ngrok or similar reverse proxies.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only redirect if:
        # 1. We're in DEBUG mode
        # 2. The request scheme is HTTP (not HTTPS) 
        # 3. X-Forwarded-Proto header indicates HTTPS is available (ngrok case)
        # 4. The host is an ngrok domain (to avoid redirecting localhost)
        host = request.get_host()
        is_ngrok = 'ngrok' in host or 'ngrok-free.dev' in host
        
        if (settings.DEBUG and 
            request.scheme == 'http' and 
            request.META.get('HTTP_X_FORWARDED_PROTO') == 'https' and
            is_ngrok):
            
            # Build the HTTPS URL
            https_url = f"https://{host}{request.get_full_path()}"
            return HttpResponsePermanentRedirect(https_url)
            
        response = self.get_response(request)
        return response