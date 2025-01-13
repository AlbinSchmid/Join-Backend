from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Wenn der User gerade erstellt wurde, erstelle auch ein UserProfile
        UserProfile.objects.create(user=instance)

# Signal zum Speichern des UserProfile, wenn der User gespeichert wird
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class Contacts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, default=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='contacts') # durch related_name könennw wir von UserProfileSerializer darauf zugreifen

    def __str__(self):
        return f'{self.name} ({self.email})'
    

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    date = models.DateField(auto_now_add=True)
    prio = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
    

class Subtask(models.Model):
    title = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title


