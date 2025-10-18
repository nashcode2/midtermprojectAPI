"""
API Project - Main Views Module
===============================

This module contains all the API endpoints and view functions for the project.
It demonstrates:
- Django REST Framework integration
- External API consumption
- User authentication
- Data processing and manipulation
- Error handling and validation

Author: [Your Name]
Course: IT312 - Web Development
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import qrcode
from io import BytesIO
import base64
import requests
import os
import secrets
import string
import random
import colorsys
from PIL import Image, ImageDraw
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
import urllib.parse
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Custom view for social account authentication errors
def social_account_error(request, provider=None):
    """
    Handle social account authentication errors with better debugging
    """
    context = {
        'provider': provider or 'Unknown',
        'debug': settings.DEBUG,
        'exception': request.GET.get('error', 'Authentication failed'),
        'error_description': request.GET.get('error_description', ''),
    }
    
    # Log the error for debugging
    logger.error(f"Social auth error for provider {provider}: {context['exception']}")
    
    return render(request, 'socialaccount/authentication_error.html', context)

# Dashboard view


@login_required
def dashboard(request):
    """
    Dashboard View - Main application interface
    
    This view renders the main dashboard with all API tools.
    It includes a timestamp for cache-busting static files.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered dashboard template with context
    """
    import time
    context = {
        'timestamp': int(time.time())  # Cache-busting for static files
    }
    return render(request, 'main/dashboard.html', context)


def home(request):
    if request.user.is_authenticated:
        return redirect('/api/dashboard/')
    return redirect('/accounts/login/')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


@login_required
def settings_page(request):
    return render(request, 'main/settings.html')


# 2FA TOTP
# 2FA TOTP setup and verify functions removed for presentation

# APIs


@api_view(['GET'])
def generate_qr(request):
    text = request.GET.get('text', 'Hello')
    use_encrypt = request.GET.get('encrypt', 'false').lower() in ('1', 'true', 'yes')
    algorithm = request.GET.get('algo', 'caesar')
    shift = int(request.GET.get('shift', '3'))

    payload = text
    if use_encrypt and algorithm == 'caesar':
        def caesar_char(ch: str, k: int) -> str:
            if 'a' <= ch <= 'z':
                return chr((ord(ch) - 97 + k) % 26 + 97)
            if 'A' <= ch <= 'Z':
                return chr((ord(ch) - 65 + k) % 26 + 65)
            return ch
        payload = ''.join(caesar_char(c, shift) for c in text)

    img = qrcode.make(payload)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return Response({'qr_code': img_str, 'content': payload, 'encrypted': use_encrypt, 'algo': algorithm})


@api_view(['GET'])
def joke(request):
    res = requests.get('https://v2.jokeapi.dev/joke/Any')
    return Response(res.json())


@api_view(['GET'])
def weather(request):
    city = request.GET.get('city', 'Manila')
    # Free, no-key weather using wttr.in
    try:
        res = requests.get(f'https://wttr.in/{city}?format=j1', timeout=10)
        data = res.json()
        current = data['current_condition'][0]
        result = {
            'name': city,
            'main': {
                'temp': float(current['temp_C'])
            },
            'weather': [
                {'description': current['weatherDesc'][0]['value']}
            ]
        }
        return Response(result)
    except Exception as exc:
        return Response({'error': 'Weather service unavailable', 'detail': str(exc)}, status=502)


@api_view(['GET'])
def cipher(request):
    text = request.GET.get('text', 'hello')
    cipher_text = ''.join(
        [chr((ord(c)-97+3) % 26+97) if c.islower() else c for c in text])
    return Response({'ciphertext': cipher_text})


# 2FA TOTP functionality removed for presentation


# New API Endpoints
@api_view(['GET'])
def news(request):
    """Get latest news headlines"""
    try:
        # Using NewsAPI (free tier) - you'll need to get an API key
        api_key = os.getenv('NEWS_API_KEY', 'demo')
        if api_key == 'demo':
            return Response({
                'articles': [
                    {'title': 'Demo News Article', 'description': 'This is a demo news article. Get a free API key from newsapi.org to see real news.', 'url': '#'},
                    {'title': 'Technology Update', 'description': 'Latest technology trends and updates in the industry.', 'url': '#'}
                ]
            })
        
        category = request.GET.get('category', 'technology')
        res = requests.get(f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}', timeout=10)
        data = res.json()
        return Response(data)
    except Exception as exc:
        return Response({'error': 'News service unavailable', 'detail': str(exc)}, status=502)


@api_view(['GET'])
def currency(request):
    """Convert currency using free exchange rate API"""
    try:
        from_curr = request.GET.get('from', 'USD')
        to_curr = request.GET.get('to', 'EUR')
        amount = float(request.GET.get('amount', 1))
        
        res = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_curr}', timeout=10)
        data = res.json()
        
        if to_curr in data['rates']:
            converted = amount * data['rates'][to_curr]
            return Response({
                'from': from_curr,
                'to': to_curr,
                'amount': amount,
                'converted': round(converted, 2),
                'rate': data['rates'][to_curr]
            })
        else:
            return Response({'error': 'Invalid currency code'}, status=400)
    except Exception as exc:
        return Response({'error': 'Currency service unavailable', 'detail': str(exc)}, status=502)


@api_view(['GET'])
def ip_info(request):
    """Get IP geolocation information"""
    try:
        ip = request.GET.get('ip', request.META.get('REMOTE_ADDR', ''))
        if not ip:
            return Response({'error': 'No IP address provided'}, status=400)
            
        res = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
        data = res.json()
        return Response(data)
    except Exception as exc:
        return Response({'error': 'IP service unavailable', 'detail': str(exc)}, status=502)


@api_view(['GET'])
def password_generator(request):
    """Generate secure passwords"""
    
    length = int(request.GET.get('length', 12))
    include_symbols = request.GET.get('symbols', 'true').lower() == 'true'
    include_numbers = request.GET.get('numbers', 'true').lower() == 'true'
    include_uppercase = request.GET.get('uppercase', 'true').lower() == 'true'
    
    chars = string.ascii_lowercase
    if include_uppercase:
        chars += string.ascii_uppercase
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    password = ''.join(secrets.choice(chars) for _ in range(length))
    
    return Response({
        'password': password,
        'length': length,
        'strength': 'strong' if length >= 12 and include_symbols else 'medium'
    })


@api_view(['GET'])
def color_palette(request):
    """Generate color palettes"""
    
    base_hue = int(request.GET.get('hue', random.randint(0, 360)))
    palette_type = request.GET.get('type', 'complementary')
    
    def hsl_to_hex(h, s, l):
        r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    colors = []
    if palette_type == 'complementary':
        colors = [
            hsl_to_hex(base_hue, 70, 50),
            hsl_to_hex((base_hue + 180) % 360, 70, 50),
            hsl_to_hex(base_hue, 50, 30),
            hsl_to_hex((base_hue + 180) % 360, 50, 30),
            hsl_to_hex(base_hue, 30, 80)
        ]
    elif palette_type == 'triadic':
        colors = [
            hsl_to_hex(base_hue, 70, 50),
            hsl_to_hex((base_hue + 120) % 360, 70, 50),
            hsl_to_hex((base_hue + 240) % 360, 70, 50),
            hsl_to_hex(base_hue, 50, 30),
            hsl_to_hex((base_hue + 120) % 360, 50, 30)
        ]
    else:  # analogous
        colors = [
            hsl_to_hex(base_hue, 70, 50),
            hsl_to_hex((base_hue + 30) % 360, 70, 50),
            hsl_to_hex((base_hue - 30) % 360, 70, 50),
            hsl_to_hex(base_hue, 50, 30),
            hsl_to_hex((base_hue + 15) % 360, 50, 30)
        ]
    
    return Response({
        'colors': colors,
        'type': palette_type,
        'base_hue': base_hue
    })


@api_view(['GET'])
def user_stats(request):
    """Get user activity statistics"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    # This would typically come from a database
    stats = {
        'total_api_calls': request.session.get('api_calls', 0),
        'qr_codes_generated': request.session.get('qr_generated', 0),
        'last_login': request.user.last_login.isoformat() if request.user.last_login else None,
        'account_created': request.user.date_joined.isoformat(),
        'preferred_city': request.session.get('last_city', 'Manila')
    }
    
    return Response(stats)


@api_view(['POST'])
def update_profile(request):
    """Update user profile information"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    # In a real app, you'd update the user model
    # For demo, we'll just update session data
    if 'preferred_city' in request.data:
        request.session['last_city'] = request.data['preferred_city']
    
    return Response({'message': 'Profile updated successfully'})

# --- Custom Facebook OAuth flow (restored) ---

def _get_facebook_app_credentials():
    """Resolve Facebook App credentials from SocialApp or environment/settings."""
    try:
        from allauth.socialaccount.models import SocialApp
        fb_app = SocialApp.objects.filter(provider='facebook').first()
        if fb_app:
            return fb_app.client_id, fb_app.secret
    except Exception:
        pass
    client_id = os.getenv('FACEBOOK_APP_ID') or getattr(settings, 'FACEBOOK_APP_ID', None)
    client_secret = os.getenv('FACEBOOK_APP_SECRET') or getattr(settings, 'FACEBOOK_APP_SECRET', None)
    return client_id, client_secret


def facebook_login(request):
    client_id, _ = _get_facebook_app_credentials()
    if not client_id:
        return HttpResponseBadRequest('Facebook is not configured')

    redirect_uri = getattr(
        settings,
        'FACEBOOK_REDIRECT_URI',
        request.build_absolute_uri(reverse('main:facebook_callback')),
    )
    scope = getattr(settings, 'FACEBOOK_SCOPES', 'public_profile,email')
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'response_type': 'code',
    }
    url = 'https://www.facebook.com/v19.0/dialog/oauth?' + urllib.parse.urlencode(params)
    return HttpResponseRedirect(url)


def facebook_callback(request):
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Facebook authentication failed: missing code')
        return redirect('/accounts/login/')

    client_id, client_secret = _get_facebook_app_credentials()
    if not client_id or not client_secret:
        messages.error(request, 'Facebook is not configured')
        return redirect('/accounts/login/')

    redirect_uri = getattr(
        settings,
        'FACEBOOK_REDIRECT_URI',
        request.build_absolute_uri(reverse('main:facebook_callback')),
    )
    token_url = 'https://graph.facebook.com/v19.0/oauth/access_token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code,
    }
    try:
        token_resp = requests.get(token_url, params=data, timeout=10)
        token_resp.raise_for_status()
        access_token = token_resp.json().get('access_token')
        if not access_token:
            messages.error(request, 'Facebook authentication failed: no access token')
            return redirect('/accounts/login/')

        profile_resp = requests.get(
            'https://graph.facebook.com/v19.0/me',
            params={'fields': 'id,name,email,picture', 'access_token': access_token},
            timeout=10,
        )
        profile_resp.raise_for_status()
        request.session['fb_profile'] = profile_resp.json()
        messages.success(request, 'Facebook login successful')
        return redirect('/accounts/login/')
    except requests.RequestException:
        messages.error(request, 'Facebook authentication failed: network error')
        return redirect('/accounts/login/')