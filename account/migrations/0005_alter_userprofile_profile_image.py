# Generated by Django 5.0 on 2024-01-19 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='uploads/user.png', null=True, upload_to='account/media/uploads/'),
        ),
    ]