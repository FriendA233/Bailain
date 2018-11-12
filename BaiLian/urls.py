from django.conf.urls import url

from BaiLian import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^myCart/$',views.myCart,name='myCart'),
    url(r'^shop/(\d+)/$',views.shop,name='shop'),
    url(r'^addcart/$',views.addcart,name='addcart'),
    url('^jiancart/$',views.jaincart,name='jiancart'),
    url('^changestatus/$',views.changestatus,name='changestatus'),
    url('^allchange/$',views.allchange,name='allchange'),
    url('^generateorder/$',views.generateorder,name='generateorder'),
    url('^orderinfo/(\d+)/$',views.orderinfo,name='orderinfo'),
    url('^pay/$',views.pay,name='pay'),        #支付
    url('^notifyurl/$',views.notifyurl,name='notifyurl'),  #支付完成后的通知
    url('^returnurl/$',views.returnurl,name='returnurl')  #支付完成后的通知
]