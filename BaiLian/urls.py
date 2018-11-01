from django.conf.urls import url

from BaiLian import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^car/$',views.car,name='car'),
    url(r'^myCart/$',views.myCart,name='myCart'),
    url(r'^shop/(\d+)/$',views.shop,name='shop'),
    # url(r'^shopwhat/(\d+)/$',views.shopwhat,name='shopwhat'),
]