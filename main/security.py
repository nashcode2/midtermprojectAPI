"""
Add security headers and debug middleware to Django application.

This middleware:
1. Adds HSTS header to force browsers to use HTTPS
2. Prints debug information about the request protocol
3. Logs OAuth related requests for debugging
"""

import logging
from django.http import HttpResponse
from django.conf import settings

# Configure logging
logger = logging.getLogger('oauth_debug')
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [OAUTH_DEBUG] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

class SecurityHeadersMiddleware:
    """Add security headers and debug OAuth request issues."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log protocol information for debugging
        protocol = "https" if request.is_secure() else "http"
        forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO', 'none')
        
        # Log OAuth-related requests to help debug Facebook login issues
        if '/accounts/' in request.path or '/facebook/' in request.path or 'oauth' in request.path.lower():
            full_url = f"{protocol}://{request.get_host()}{request.path}"
            logger.debug(f"OAuth Request: {request.method} {full_url}")
            logger.debug(f"Protocol: {protocol}, X-Forwarded-Proto: {forwarded_proto}")
            logger.debug(f"Is secure: {request.is_secure()}")
            logger.debug(f"Headers: Host={request.META.get('HTTP_HOST')}")
        
        # Get the response
        response = self.get_response(request)
        
        # Add security headers
        if not settings.DEBUG:
            # In production, use a more strict HSTS policy
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        else:
            # In development, use a shorter HSTS for testing
            response['Strict-Transport-Security'] = 'max-age=3600'
        
        return response