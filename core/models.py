from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} : {self.title}'
    
    class Meta:
        ordering = ['id']


class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)

    
    def __str__(self):
        return f'Perfil de {self.user.username}'

class Message(models.Model):
    envia = models.ForeignKey(User, on_delete=models.CASCADE, related_name='envia')
    recibe = models.ForeignKey(User, on_delete=models.CASCADE,related_name='recibe')
    content = models.TextField(blank=False, null=False)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.content
    