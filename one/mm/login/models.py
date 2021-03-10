import random

from django.db import models

# Create your models here.

def default_sign():
    signs = ['../static/images/1.png',
             '../static/images/2.png',
             '../static/images/3.png',
             '../static/images/4.png',
             '../static/images/5.png',
             '../static/images/6.png',
             '../static/images/7.png',
             '../static/images/8.png',
             '../static/images/9.png',
             '../static/images/10.png',
             '../static/images/11.png',
             '../static/images/12.png',
             '../static/images/13.png',
             '../static/images/14.png',
             '../static/images/15.png',
             '../static/images/16.png',
             '../static/images/17.png',
             '../static/images/18.png',
             '../static/images/19.png',
             '../static/images/20.png',
             '../static/images/21.png',
             '../static/images/22.png',
             '../static/images/23.png',
             '../static/images/24.png',
             '../static/images/25.png',
             '../static/images/35.png',

             ]

    return random.choice(signs)
class User(models.Model):
    username = models.CharField('姓名', max_length=11, primary_key=True)
    nickname = models.CharField('昵称', max_length=30)
    email = models.EmailField()
    password = models.CharField('密码',max_length=32)
    # avatar = models.ImageField('头像',upload_to='avatar', null=True)
    avatar = models.CharField('头像',max_length=150,default=default_sign)
    created_time = models.DateTimeField('注册时间',auto_now_add=True)
    phone = models.CharField(max_length=11, default='')
    vip=models.BooleanField('会员状态',default=False)
    problem=models.CharField('问题',max_length=90)
    key=models.CharField('答案',max_length=50)
