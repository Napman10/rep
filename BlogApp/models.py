from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    manager = models.Manager()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    text = models.TextField(max_length=None, null=False)
    author_name = models.CharField(max_length=50, null=False)
    datetime = models.DateTimeField(auto_now=True)

class UserImage(models.Model):
    manager = models.Manager()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    photo = models.ImageField(upload_to='users', blank=True, null=True)

class UserStatus(models.Model):
    manager = models.Manager()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(max_length=100, null=True)
    
# Create your models here.
