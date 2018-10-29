import hashlib
import random
import time
import uuid

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from BaiLian.models import User


def index(request):
    return render(request,'index.html')


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


def car(request):
    return render(request,'car.html')


def myCart(request):
    return render(request,'myCart.html')


def shop(request):
    return render(request,'shop.html')


def shopwhat(request):
    return render(request,'shopwhat.html')