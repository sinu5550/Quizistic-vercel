from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='account/media/uploads/',default='account/media/uploads/user.png', blank = True, null = True)

    def __str__(self):
        return self.user.username
