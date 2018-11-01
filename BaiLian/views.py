import hashlib
import random
import time
import uuid

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from BaiLian.models import User, Goods


def index(request):
    goods_list = Goods.objects.all()
    token = request.COOKIES.get('token')
    users = User.objects.filter(token=token)
    if users.exists():
        user = users.first()
        return render(request, 'index.html', context={'username': user.username,'goods_list':goods_list})
    else:
        return render(request, 'index.html',context={'goods_list':goods_list})


def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()

def generate_token():
    token = str(time.time()) + str(random.random())
    # MD5
    md5 = hashlib.md5()
    md5.update(token.encode('utf-8'))
    return md5.hexdigest()
#注册
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tel = request.POST.get('tel')
        mail = request.POST.get('E-mail')

        #存入数据库
        try:
            user = User()
            user.username = username
            #加密处理
            user.password = generate_password(password)
            user.tel = tel
            user.mail = mail
            user.token = uuid.uuid5(uuid.uuid4(), 'register')
            user.save()

            #重定向
            response = redirect('bl:index')

            #状态保持
            response.set_cookie('token',user.token)

            return response
        except Exception as e:
            return HttpResponse('注册失败' + e)


#登陆
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        #验证
        password = generate_password(request.POST.get('password'))

        users = User.objects.filter(username=username,password=password)

        if users.exists():
            user = users.first()

            #token
            user.token = generate_token()

            user.save()

            #重定向
            response = redirect('bl:index')
            response.set_cookie('token',user.token)

            return response
        else:
            return HttpResponse('用户名或密码错误')

#退出
def logout(request):
    response = redirect('bl:index')
    response.delete_cookie('token')

    return response

def car(request):
    return render(request,'car.html')


def myCart(request):
    return render(request,'myCart.html')


def shop(request,id = 1):
    good = Goods.objects.filter(id=id).all().first()
    return render(request,'shop.html',context={'good':good})


def shopwhat(request,id):
    good = Goods.objects.filter(id = id).all().first()
    return render(request,'shopwhat.html',context={'good':good})


