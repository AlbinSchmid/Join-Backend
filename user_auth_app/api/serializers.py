from user_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email') # DATA: daten die wir übergeben haben (data=request.data)
        password = data.get('password')
        user = authenticate(email=email, password=password) # wird von unser eigenen Backend ausgeführt in der backends.py, haben die in settings verändert

        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError('No user found')
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta: 
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        pw = self.validated_data['password']
        reapeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']
        username = self.validated_data['username']

        if pw != reapeated_pw:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        account = User(email=email, username=username)
        account.set_password(pw)
        account.save()
        return account