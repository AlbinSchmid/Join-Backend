from user_auth_app.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    # Hier wird auf den Model Contacts auf das feld mit related_name='contacts' zugegriffen
    contacts = serializers.StringRelatedField(many=True, read_only=True)
    contact_count = serializers.SerializerMethodField()
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    def get_contact_count(self, obj):
        return obj.contacts.count()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'user_email',
                  'contact_count', 'contacts', 'tasks']


class SubtaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    task = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subtask
        fields = ['id', 'title', 'completed', 'task']


class SubtaskCreateSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        write_only=True,
        source='task',
    )

    class Meta:
        model = Subtask
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        write_only=True,
        source='user'
    )

    class Meta:
        model = Contacts
        fields = ['id', 'name', 'email', 'phone',
                  'color', 'tasks', 'user', 'user_id']


class ContactHyperlinkSerializer(ContactSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contacts
        fields = ['url', 'name', 'email', 'phone']


class EditContactTaskSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        write_only=True,
        source='user'
    )
    contact_ids = serializers.PrimaryKeyRelatedField(
        queryset=Contacts.objects.all(),
        many=True,
        write_only=True,
        source='contacts'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date', 'prio', 'category',
                  'taskCategory', 'subtasks', 'contacts', 'contact_ids', 'user', 'user_id']


class TaskSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        write_only=True,
        source='user'
    )
    contact_ids = serializers.PrimaryKeyRelatedField(
        queryset=Contacts.objects.all(),
        many=True,
        write_only=True,
        source='contacts'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date', 'prio', 'category',
                  'taskCategory', 'subtasks', 'contacts', 'contact_ids', 'user', 'user_id']

    def create(self, validated_data):
        # subtasks und contacts sind verwandte Objekte, die nicht direkt als Teil der Hauptdaten für Task gespeichert werden. Sie müssen getrennt behandelt werden, weil sie eine Beziehung zu anderen Modellen haben.
        subtasks_data = validated_data.pop('subtasks', [])
        contacts_data = validated_data.pop('contacts', [])

        # validated_data enthält alle anderen Felder, die mit dem Task-Modell zu tun haben, wie title, description, prio, usw. Task.objects.create() erstellt ein neues Task-Objekt in der Datenbank mit diesen Daten.
        task = Task.objects.create(**validated_data)

        # contacts_data enthält die Kontakte, die wir vorher aus den validated_data entfernt haben. Ein Task kann viele Contacts haben, daher verwenden wir set(), um diese Kontakte mit dem Task zu verbinden.
        task.contacts.set(contacts_data)

        # Für jede Subtask in subtasks_data wird ein neues Subtask-Objekt erstellt, wobei der task-ForeignKey automatisch auf das gerade erstellte Task gesetzt wird. Das bedeutet, jede Subtask wird mit dem entsprechenden Task verknüpf
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def update(self, instance, validated_data): 
        subtasks_data = validated_data.pop('subtasks', None)  
        contact_ids_data = validated_data.pop('contact_ids', None)

        for attr, value in validated_data.items():  
            setattr(instance, attr, value)  
        instance.save()  

        if subtasks_data is not None:  
            existing_subtasks = {subtask.id: subtask for subtask in instance.subtasks.all()}  
            created_subtask_ids = []  

            for subtask_data in subtasks_data:  
                subtask_id = subtask_data.get('id')  

                if subtask_id is None:  
                    new_subtask = Subtask.objects.create(task=instance, **subtask_data)  
                    created_subtask_ids.append(new_subtask.id)
                    print(f'New subtask created with id: {new_subtask.id} and data: {subtask_data}')  
                elif subtask_id in existing_subtasks:  
                    existing_subtask = existing_subtasks[subtask_id]  
                    for attr, value in subtask_data.items():  
                        setattr(existing_subtask, attr, value)  
                    existing_subtask.save()  
                    created_subtask_ids.append(existing_subtask.id)
                    print(f'Updated subtask with id: {subtask_id}')  

            for subtask_id in existing_subtasks.keys():  
                if subtask_id not in created_subtask_ids:  
                    existing_subtasks[subtask_id].delete()
                    print(f'Deleted subtask with id: {subtask_id}')  
        return instance

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    id = serializers.IntegerField(source='user.id', read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
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
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists'})

        account = User(email=email, username=username)
        account.set_password(pw)
        account.save()
        return account
