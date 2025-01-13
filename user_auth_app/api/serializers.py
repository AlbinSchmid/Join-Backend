from user_auth_app.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    contacts = serializers.StringRelatedField(many=True, read_only=True) # Hier wird auf den Model Contacts auf das feld mit related_name='contacts' zugegriffen
    contact_count = serializers.SerializerMethodField()
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    def get_contact_count(self, obj):
        return obj.contacts.count()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'user_email','contact_count', 'contacts', 'tasks']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        write_only=True,
        source='user'
    )
    subtasks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta: 
        model = Task
        fields = ['id', 'title', 'description', 'date', 'prio', 'category', 'subtasks', 'user', 'user_id']


class TaskHyperlinkSerializer(TaskSerializer ,serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Task
        fields = ['url', 'title', 'description', 'date', 'prio', 'category', 'subtasks', 'user', 'user_id']


class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        write_only=True,
        source='task'
    )

    class Meta: 
        model = Subtask
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        write_only=True,
        source='user'
    )

    class Meta:
        model = Contacts
        fields = ['id', 'name', 'email', 'phone', 'user', 'user_id']


class ContactHyperlinkSerializer(ContactSerializer ,serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Contacts
        fields = ['url', 'name', 'email', 'phone']


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