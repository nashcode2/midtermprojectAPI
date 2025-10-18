#!/usr/bin/env python
"""
Script to set up OAuth Social Apps for Facebook and Google
Run this after creating a superuser: python manage.py createsuperuser
Then run: python setup_oauth.py
"""

import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_nash_project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from dotenv import load_dotenv

# Load environment variables
load_dotenv(BASE_DIR / '.env')

def setup_oauth_apps():
    # Get or create the default site
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={
            'domain': 'pseudophilanthropic-vanda-hatlike.ngrok-free.dev',
            'name': 'API Nash Project'
        }
    )
    
    # Update site domain if using ngrok
    if site.domain != 'pseudophilanthropic-vanda-hatlike.ngrok-free.dev':
        site.domain = 'pseudophilanthropic-vanda-hatlike.ngrok-free.dev'
        site.save()
        print(f"Updated site domain to: {site.domain}")
    
    # Clean up existing Facebook apps and create a new one
    facebook_app_id = os.getenv('FACEBOOK_APP_ID')
    facebook_app_secret = os.getenv('FACEBOOK_APP_SECRET')
    
    if facebook_app_id and facebook_app_secret:
        # Remove existing Facebook apps
        SocialApp.objects.filter(provider='facebook').delete()
        print("Cleaned up existing Facebook apps")
        
        # Create new Facebook app
        facebook_app = SocialApp.objects.create(
            provider='facebook',
            name='Facebook',
            client_id=facebook_app_id,
            secret=facebook_app_secret,
        )
        facebook_app.sites.add(site)
        print(f"✅ Facebook OAuth configured with App ID: {facebook_app_id}")
    else:
        print("❌ Facebook credentials not found in .env file")
    
    # Clean up existing Google apps and create a new one
    google_client_id = os.getenv('GOOGLE_CLIENT_ID')
    google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if google_client_id and google_client_secret and google_client_id != 'your_google_client_id_here':
        # Remove existing Google apps
        SocialApp.objects.filter(provider='google').delete()
        print("Cleaned up existing Google apps")
        
        # Create new Google app
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id=google_client_id,
            secret=google_client_secret,
        )
        google_app.sites.add(site)
        print(f"✅ Google OAuth configured with Client ID: {google_client_id}")
    else:
        print("❌ Google credentials not found or not configured in .env file")
        print("   Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env file")
    
    print("\n🚀 OAuth setup complete!")
    print(f"Site configured for: {site.domain}")
    print("\nNext steps:")
    print("1. Make sure your ngrok tunnel is running: ngrok http 8000")
    print("2. Update Facebook app settings with the ngrok URL")
    print("3. Start your Django server: python manage.py runserver")
    print("4. Visit: https://pseudophilanthropic-vanda-hatlike.ngrok-free.dev/accounts/login/")

if __name__ == '__main__':
    setup_oauth_apps()