# Generated by Django 5.0 on 2024-01-19 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userprofile_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_image',
        ),
    ]
