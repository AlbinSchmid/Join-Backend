from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        # CHECK_PASSWORD: Die Passwörter werden in der Datenbank gehasht gespeichert, check_password vergleicht das gehashte Passwort in der Datenbank mit dem gehashten Wert des eingegebenen Passworts.
        if user.check_password(password):
            return user
        return None