from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    tel = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    #唯一标识令牌
    token = models.CharField(max_length=256,default='')
