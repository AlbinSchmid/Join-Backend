# Generated by Django 5.1.4 on 2025-01-16 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0008_task_taskcategory_alter_contacts_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='contacts',
            field=models.ManyToManyField(related_name='tasks', to='user_auth_app.contacts'),
        ),
    ]
