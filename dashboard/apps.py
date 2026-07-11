from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """AppConfig for the auto-created `dashboard` app.

    This minimal config uses the app label 'dashboard' to match
    the entry in `INSTALLED_APPS` so Django can import it.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
