from rest_framework import generics
from user_auth_app.models import UserProfile, Contacts
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class SubtaskListView(generics.ListCreateAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskHyperlinkSerializer


class TasksOfUserListView(generics.ListCreateAPIView):
    serializer_class = TaskHyperlinkSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user_profile = UserProfile.objects.get(pk=pk)
        return user_profile.tasks.all()


class ContactsOfUserListView(generics.ListCreateAPIView):
    serializer_class = ContactHyperlinkSerializer

    # bekommen die Sellers von den Market
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user_profile = UserProfile.objects.get(pk=pk)
        return user_profile.contacts.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        market = UserProfile.objects.get(pk=pk)
        serializer.save(UserProfile=[UserProfile])


class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(generics.RetrieveAPIView, generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
    queryset = UserProfile.objects.all()    
    serializer_class = UserProfileSerializer


class ContactListView(generics.ListCreateAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactHyperlinkSerializer


class ContactDetailView(generics.RetrieveAPIView, generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactSerializer


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