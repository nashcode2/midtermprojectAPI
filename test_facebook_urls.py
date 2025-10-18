#!/usr/bin/env python
"""
Test Facebook OAuth URLs and Configuration
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
from allauth.socialaccount.providers.facebook.views import oauth2_login
from django.urls import reverse
from django.test import RequestFactory

def test_facebook_urls():
    print("🧪 Testing Facebook OAuth URLs")
    print("=" * 50)
    
    # Get site and app info
    site = Site.objects.get(pk=1)
    facebook_app = SocialApp.objects.get(provider='facebook')
    
    base_url = f"https://{site.domain}"
    
    # Test URLs
    login_url = f"{base_url}/accounts/facebook/login/"
    callback_url = f"{base_url}/accounts/facebook/login/callback/"
    
    print(f"✅ Site Domain: {site.domain}")
    print(f"✅ Facebook App ID: {facebook_app.client_id}")
    print(f"✅ Login URL: {login_url}")
    print(f"✅ Callback URL: {callback_url}")
    
    print(f"\n📋 Facebook App Configuration Checklist:")
    print(f"   1. Go to: https://developers.facebook.com/apps/{facebook_app.client_id}/fb-login/settings/")
    print(f"   2. Enable 'Client OAuth Login': ✓")
    print(f"   3. Enable 'Web OAuth Login': ✓")
    print(f"   4. Add to 'Valid OAuth Redirect URIs':")
    print(f"      {callback_url}")
    print(f"   5. Go to: https://developers.facebook.com/apps/{facebook_app.client_id}/settings/basic/")
    print(f"   6. Add to 'App Domains':")
    print(f"      {site.domain}")
    print(f"   7. Set App Mode to 'Development' (for testing)")
    print(f"   8. Add yourself as App Developer/Tester")
    
    print(f"\n🔗 Direct Links:")
    print(f"   Facebook Login Settings: https://developers.facebook.com/apps/{facebook_app.client_id}/fb-login/settings/")
    print(f"   App Basic Settings: https://developers.facebook.com/apps/{facebook_app.client_id}/settings/basic/")
    print(f"   App Roles: https://developers.facebook.com/apps/{facebook_app.client_id}/roles/")

if __name__ == '__main__':
    test_facebook_urls()