from typing import Dict

def social_providers(request) -> Dict[str, bool]:
    try:
        from allauth.socialaccount.models import SocialApp
        has_google = SocialApp.objects.filter(provider='google').exists()
        # Facebook enabled
        has_facebook = SocialApp.objects.filter(provider='facebook').exists()
        return {
            'social_google_enabled': has_google,
            'social_facebook_enabled': has_facebook,
        }
    except Exception:
        return {
            'social_google_enabled': False,
            'social_facebook_enabled': False,
        }


