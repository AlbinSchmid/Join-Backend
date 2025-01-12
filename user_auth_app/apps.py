from django.apps import AppConfig

class UserAuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_auth_app'

    def ready(self):
        import user_auth_app.models  # Ersetze 'your_app' durch den Namen deiner App
