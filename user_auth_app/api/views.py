from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, EmailLoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny] # Sagen hier das es immer anwenden darf

    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data) # der Serializer der dan später ausgeführt bei serializer.is_valid()
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email
            }
        else: 
            data=serializer.errors

        return Response(data)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            save_user = serializer.save()
            token, create = Token.objects.get_or_create(user=save_user)
            data = {
                'token': token.key,
                'username': save_user.username,
                'email': save_user.email
            }
        else: 
            data=serializer.errors

        return Response(data)