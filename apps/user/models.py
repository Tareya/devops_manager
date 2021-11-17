from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class UserProfile(AbstractUser):
    '''
    用户信息 资源模型
    '''

    username = models.CharField()
    password = models.CharField()
    email    = models.EmailField()
