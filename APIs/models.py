from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    picture = models.FileField(blank=True, null=True, upload_to='Profile_pics/')

class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete= models.CASCADE),
    amount = models.IntegerField(),
    currency = models.CharField(),
    receiver = models.CharField(),
    account = models.CharField(),
    transfer_date = models.DateTimeField(auto_now_add= True)