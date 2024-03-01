from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=25,unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.name