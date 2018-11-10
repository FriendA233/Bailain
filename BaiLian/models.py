from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    tel = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    #唯一标识令牌
    token = models.CharField(max_length=256,default='')



class Goods(models.Model):
    indeximg = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    cost = models.CharField(max_length=50)
    init = models.CharField(max_length=10)
    img1 = models.CharField(max_length=255)
    img2 = models.CharField(max_length=255)
    img3 = models.CharField(max_length=255)
    img4 = models.CharField(max_length=255)


class Slideshow(models.Model):
    img = models.CharField(max_length=100)



class Cart(models.Model):
    user = models.ForeignKey(User)
    goods =models.ForeignKey(Goods)
    number = models.IntegerField()
    isselect = models.BooleanField(default=True)


