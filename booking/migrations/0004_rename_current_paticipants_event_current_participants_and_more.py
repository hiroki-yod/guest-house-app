# Generated by Django 4.1.7 on 2023-03-23 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_rename_event_application_eventapplication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='current_paticipants',
            new_name='current_participants',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='max_paticipants',
            new_name='max_participants',
        ),
    ]