from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Ensure static directory exists at runtime (dev convenience)
        import os
        from django.conf import settings
        static_app_dir = os.path.join(settings.BASE_DIR, 'main', 'static', 'main')
        os.makedirs(static_app_dir, exist_ok=True)

        # Defer any database work to signals to avoid DB access during app init
        try:
            # Import connects signal handlers (no DB access on import)
            from . import signals  # noqa: F401
        except Exception:
            # In case optional deps are missing in certain environments
            pass