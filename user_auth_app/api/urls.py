from django.urls import path, include
from .views import *

urlpatterns = [
    path('', UserProfileList.as_view()),
    path('signUp/', RegistrationView.as_view(), name='registration'),
    path('logIn/', CustomLoginView.as_view(), name='logIn'),
]