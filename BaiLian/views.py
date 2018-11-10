import hashlib
import random
import time
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from BaiLian.models import User, Goods, Slideshow, Cart


def index(request):
    goods_list = Goods.objects.all()
    slideshow = Slideshow.objects.all()
    token = request.COOKIES.get('token')
    users = User.objects.filter(token=token)
    if users.exists():
        user = users.first()
        return render(request, 'index.html',
                      context={'username': user.username, 'goods_list': goods_list, 'slideshow': slideshow})
    else:
        return render(request, 'index.html', context={'goods_list': goods_list, 'slideshow': slideshow, 'token': token})


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


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tel = request.POST.get('tel')
        mail = request.POST.get('E-mail')

        # 存入数据库
        try:
            user = User()
            user.username = username
            # 加密处理
            user.password = generate_password(password)
            user.tel = tel
            user.mail = mail
            user.token = uuid.uuid5(uuid.uuid4(), 'register')
            user.save()

            # 重定向
            response = redirect('bl:index')

            # 状态保持
            response.set_cookie('token', user.token)

            return response
        except Exception as e:
            return HttpResponse('注册失败' + e)


# 登陆
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        # 验证
        password = generate_password(request.POST.get('password'))

        users = User.objects.filter(username=username, password=password)

        if users.exists():
            user = users.first()

            # token
            user.token = generate_token()

            user.save()

            # 重定向
            response = redirect('bl:index')
            response.set_cookie('token', user.token)

            return response
        else:
            return HttpResponse('用户名或密码错误')


# 退出
def logout(request):
    response = redirect('bl:index')
    response.delete_cookie('token')

    return response


def myCart(request):
    token = request.COOKIES.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)
        paer = 0
        for cart in carts:
            if not cart.isselect:
                continue
            paer += int(cart.number) * int(cart.goods.price)
        return render(request, 'myCart.html', context={'carts': carts, 'pager': paer})
    else:
        return redirect('bl:login')


def shop(request, id=1):
    good = Goods.objects.filter(id=id).all().first()
    token = request.COOKIES.get('token')
    user = User.objects.filter(token=token)
    cart = Cart.objects.filter(user=user).filter(goods=good).first()
    return render(request, 'shop.html', context={'good': good, 'cart': cart})


def shopwhat(request, id):
    good = Goods.objects.filter(id=id).all().first()
    return render(request, 'shopwhat.html', context={'good': good})


def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.COOKIES.get('token')
    print(token)
    responseData = {
        'msg': '添加购物车成功',
        'status': 1,
    }
    if token:
        # 用户
        user = User.objects.get(token=token)
        # 商品
        goods = Goods.objects.get(pk=goodsid)
        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number'] = cart.number

        else:
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()
            responseData['number'] = cart.number
        return JsonResponse(responseData)
    else:
        responseData['msg'] = '未登录,请登陆后操作'
        responseData['status'] = -1
    return JsonResponse(responseData)


def jaincart(request):
    goodsid = request.GET.get('goodsid')
    token = request.COOKIES.get('token')
    responseData = {
        'msg': '购物车减操作成功',
        'status': 1,
    }
    if token:
        # 用户
        user = User.objects.get(token=token)
        # 商品
        goods = Goods.objects.get(pk=goodsid)
        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():
            cart = carts.first()
            cart.number = cart.number - 1
            cart.save()
            responseData['number'] = cart.number

        else:
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()
            responseData['number'] = cart.number
        return JsonResponse(responseData)
    else:
        responseData['msg'] = '未登录,请登陆后操作'
        responseData['status'] = -1
    return JsonResponse(responseData)


def changestatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = False if cart.isselect else True
    cart.save()
    paer = 0
    carts = Cart.objects.filter(user=User.objects.get(token=request.COOKIES.get('token')))
    for cart1 in carts:
        if not cart1.isselect:
            continue
        paer += int(cart1.number) * int(cart1.goods.price)
    responseData = {
        'msg': '选中状态改变',
        'status': 1,
        'isselect': cart.isselect,
        'paer': paer
    }
    return JsonResponse(responseData)


def allchange(request):
    isselect = False if request.GET.get('isselect') == 'true' else True
    token = request.COOKIES.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)
    paer = 0
    bom = False
    for cart in carts:
        if isselect:
            cart.isselect = False
        else:
            bom = True
            cart.isselect = True
            paer += int(cart.number) * int(cart.goods.price)
        cart.save()

    return JsonResponse({'isselect':bom,'paer':paer})

# if isselect == 'true':
#     token = request.COOKIES.get('token')
#     user = User.objects.get(token=token)
#     carts = Cart.objects.filter(user=user)
#     for cart in carts:
#         cart.isselect = 1
#         cart.save()
# else:
#     token = request.COOKIES.get('token')
#     user = User.objects.get(token=token)
#     carts = Cart.objects.filter(user=user)
#     for cart in carts:
#         cart.isselect = 0
#         cart.save()


