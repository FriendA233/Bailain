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

#订单
#一个用户对应多个订单
#在从表这声名关系
class Order(models.Model):
    # 用户
    user = models.ForeignKey(User)
    #订单创建时间
    createtime = models.DateTimeField(auto_now_add=True)
    #状态
    status = models.IntegerField(default=1)
    #订单号
    identifier = models.CharField(max_length=256)


#订单商品
#一个订单对应多个商品
#在从表中声名关系

class OrderGoods(models.Model):
    #订单
    order = models.ForeignKey(Order)
    #商品
    goods = models.ForeignKey(Goods)
    #个数
    number = models.IntegerField(default=1)

