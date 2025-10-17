from __future__ import annotations

import os
from dotenv import load_dotenv
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver


def _configure_social_apps_if_env_vars() -> None:
    # Only run if we're not in a migration or shell command
    import sys
    if 'migrate' in sys.argv or 'shell' in sys.argv or 'collectstatic' in sys.argv:
        return
        
    try:
        # Ensure .env variables are loaded for local dev
        from pathlib import Path
        project_root = Path(__file__).resolve().parents[1]
        load_dotenv(project_root / '.env')
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site
        from django.db import connection
        # Check if database is ready
        if not connection.introspection.table_names():
            return
    except Exception:
        return

    try:
        site = Site.objects.get(id=settings.SITE_ID)
    except Exception:
        return

    google_id = os.getenv('GOOGLE_CLIENT_ID')
    google_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    if google_id and google_secret:
        app, _ = SocialApp.objects.get_or_create(
            provider='google',
            name='Google OAuth',
            defaults={'client_id': google_id, 'secret': google_secret},
        )
        if site not in app.sites.all():
            app.sites.add(site)
        if app.client_id != google_id or app.secret != google_secret:
            app.client_id = google_id
            app.secret = google_secret
            app.save()

    # Facebook OAuth - will create app if credentials are provided
    fb_id = os.getenv('FACEBOOK_APP_ID') or os.getenv('FACEBOOK_CLIENT_ID')
    fb_secret = os.getenv('FACEBOOK_APP_SECRET') or os.getenv('FACEBOOK_CLIENT_SECRET')
    if fb_id and fb_secret:
        app, _ = SocialApp.objects.get_or_create(
            provider='facebook',
            name='Facebook OAuth',
            defaults={'client_id': fb_id, 'secret': fb_secret},
        )
        if site not in app.sites.all():
            app.sites.add(site)
        if app.client_id != fb_id or app.secret != fb_secret:
            app.client_id = fb_id
            app.secret = fb_secret
            app.save()


@receiver(post_migrate)
def main_post_migrate(sender, **kwargs):  # noqa: D401
    _configure_social_apps_if_env_vars()

# Note: Do not access DB at import time to avoid startup warnings.


