# Generated by Django 5.0 on 2024-01-20 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_alter_comment_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='choice',
            field=models.CharField(choices=[('⭐', '⭐'), ('⭐⭐', '⭐⭐'), ('⭐⭐⭐', '⭐⭐⭐'), ('⭐⭐⭐⭐', '⭐⭐⭐⭐'), ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐')], max_length=20),
        ),
    ]
