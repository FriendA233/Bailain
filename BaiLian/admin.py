from django.contrib import admin

# Register your models here.

from .models import Goods,User,Slideshow

admin.site.register(Goods)
admin.site.register(User)
admin.site.register(Slideshow)
