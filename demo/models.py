from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

class Message(models.Model):   
    username = models.CharField(max_length=100)
    messages = models.TextField()

    def __str__(self):
        return f'{self.username}: {self.messages}'


