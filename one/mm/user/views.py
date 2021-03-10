from django.core import mail
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.defaulttags import csrf_token
from django.utils.decorators import method_decorator
from django.views import View
import json
import hashlib
import jwt
from django.views.decorators.csrf import csrf_exempt

from tools.login_dec import login_check
from django.conf import settings
from  login.views import sms_view
from  login.views import  make_token
from tools.sms import YunTongXin

from login.models import User
import redis
import random
import string
# Create your views here.
class UsersView(View):

    def get(self,request,username=None):
        # 在数据库获取数据
        try:
            user=User.objects.get(username=username)
        except Exception as e:
            print('-get user error is %s-' % e)
        print('################################已经开始进入后端Get##################')
        print(user.created_time)
        if user.vip==0:
            vip='普通会员'
        elif user.vip==1:
            vip = '高级Vip会员'
        Y=user.created_time.strftime('%Y')
        m=user.created_time.strftime('%m')
        d=user.created_time.strftime('%d')
        created_time=(f'{Y}年{m}月{d}日')
        print('email', user.email, 'avatar',user.avatar, 'phone', user.phone)


        result = {'code': 200, 'data': {'username': user.nickname,'user_type':vip,'created_time':created_time,'phone': user.phone,'email': user.email,'avatar':user.avatar

                                        }}
        return JsonResponse(result)

    @method_decorator(login_check)
    def post(self,request,username=None):


            json_str=request.body
            json_obj=json.loads(json_str)
            username = json_obj['username']
            # email = json_obj['email']
            # phone = json_obj['phone']
            old_password=json_obj['old_password']
            print(old_password)
            password_1 = json_obj['password_1']
            print(password_1)
            password_2 = json_obj['password_2']
            print(password_2)
            if not old_password:
                result={'code':10100,'error': '原密码不为空'}
            md5 = hashlib.md5()
            md5.update(old_password.encode())
            inswept_password = md5.hexdigest()
            print(username)
            print('################################已经开始进入后端Post##################')
            try:
                user=User.objects.get(username=username)
            except Exception as e:
                print('-get user error is %s-' % e)
            # print(username, email, phone, password_1, password_2)

            # 1 验证 原密码
            if not old_password:
                result={'code':10100,'error': '原密码不为空'}
                return JsonResponse(result)
            else:
                if user.password !=inswept_password:
                    result = {'code': 10100, 'error': '原密码错误'}
                    return JsonResponse(result)

            # 2 两次密码要一致
            if not password_1 or not password_2:
                result = {'code': 10100, 'error': '密码不为空'}
                return JsonResponse(result)
            else:
                if password_1 != password_2:
                    result = {'code': 10101, 'error': '两次密码不一致！'}
                    return JsonResponse(result)
            #3 hash 处理
            md5=hashlib.md5()
            md5.update(password_1.encode())
            password_h=md5.hexdigest()
            # 4 验证数据库密码 与新密码是否一致
            if user.password==password_h:
                result = {'code': 10102, 'error': '密码一致！'}
                return JsonResponse(result)
            else:
            # 4 修改数据库密码
                user.password=password_h
                user.save()
                return JsonResponse({'code':200})


    @method_decorator(login_check)
    def put(self,request):
        print('#################在装饰器后Put ############################')
        # 1,获取用户提交的数据
        json_str = request.body
        json_obj = json.loads(json_str)
        # 2 从request.myuser中获取要修改的用户
        user = request.myuser
        user.sign = json_obj['sign']
        user.nickname = json_obj['nickname']
        user.info = json_obj['info']
        user.save()


r=redis.Redis(host='127.0.0.1',port=6379,db=0)

# @csrf_exempt
@login_check
def email_1_view(request,username):
    seeds = string.digits
    random_str = []
    for i in range(4):
        random_str.append(random.choice(seeds))
    number = "".join(random_str)
    # if r.get('validate')
    if r.exists('validate'):
        r.delete('validate')
    r.set('validate', number, ex=120)
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
        except Exception as  e:
            print('-get user error is %s-' % e)

        mail.send_mail(subject='邮箱验证码',
                       message=f'你的验证码是：{number}',
                       from_email='2602160663@qq.com',
                       recipient_list=[user.email, ])
        return JsonResponse({'code': 200})




@login_check
def email_view(request,username):
    if request.method =='POST':
        print('开始进入email_view  POST视图啦 ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥')
        json_str = request.body
        json_obj = json.loads(json_str)
        nex_email=json_obj['nex_email']
        emailValidatenum=json_obj['emailValidatenum']
        print('在 你还没有获取邮件验证码$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',nex_email)
        try:
            user=User.objects.get(username=username)
        except Exception as  e:
            print('-get user error is %s-' % e)
        if r.get('validate'):
            result = {'code': 30100, 'error': '你还没有获取邮件验证码'}
            return JsonResponse(result)

        if not nex_email:
            result = {'code': 301001, 'error': '邮箱不为空'}
            return JsonResponse(result)
        # if not email_input:
        #     result = {'code': 30102, 'error': '图片验证码不为空'}
        #     return JsonResponse(result)
        if not emailValidatenum:
            result = {'code': 30103, 'error': '邮箱验证码不为空'}
            return JsonResponse(result)
        # if email_input!=num:
        #     result = {'code': 30104, 'error': '图片验证码不正确'}
        #     return JsonResponse(result)
        if emailValidatenum ==r.get('validate'):
            user.email=nex_email
            user.save()
            return JsonResponse({'code':200})




def info_img_view(request,username):
    print(username)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 进入后端啦")
    json_str = request.body
    json_obj = json.loads(json_str)
    print('json_obj>>>>>>',json_obj)
    new_photo = json_obj['photo']
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 开始打印 new_photo")
    print(new_photo)
    try:
        user = User.objects.get(nickname=username)
    except Exception as  e:
        print('error is %s'%e)

    user.avatar=new_photo
    user.save()
    return  JsonResponse({'code':200})

def phone_updating(request,username):
    pass




@csrf_exempt
@login_check
def amend_name_view(request,username):

    if request.method=='POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        newname = json_obj['newname']
        okname = json_obj['okname']

        try:
            user = User.objects.get(username=username)
        except Exception as  e:
            print('-get user error is %s-' % e)

        if not newname:
            result = {'code': 50100, 'error': '新用户名不为空'}
            return JsonResponse(result)
        if not okname:
            result = {'code': 50101, 'error': '确认用户名不为空'}
            return JsonResponse(result)
        old_username = User.objects.filter(username=newname)
        if old_username:
            result = {'code': 50102, 'error': '用户名已被占用!'}
            return JsonResponse(result)
        old_nickname = User.objects.filter(nickname=newname)
        if old_nickname:
            result = {'code': 50102, 'error': '用户名已被占用!'}
            return JsonResponse(result)
        if newname !=okname:
            result = {'code': 50103, 'error': '两次输入不一致'}
            return JsonResponse(result)
        else:
            print(user.username,newname,'user.usernameuser.usernameuser.usernameuser.usernameuser.usernameuser.username')
            # user.username=newname
            user.nickname=newname
            user.save()

            print('￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥修改之后的user.username：',user.username)
            return  JsonResponse({'code':200})
            # 重新修改签发token
            # token = make_token(username)
            # # 字节串表示的token转换为字符串
            # token = token.decode()
            # return JsonResponse({'code':200,'username':newname,'data':{'token':token}})



@csrf_exempt
@login_check
def old_phone_view(request,username=None):
    if request.method=='POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        phone=json_obj['phone']
        noteInput=json_obj['noteInput']
        cache_key = 'sms_%s' % phone
        a = cache.get(cache_key)
        print('输入的验证码',noteInput)
        print('手机验证码 >>>>>>',a)
        if noteInput !=str(a):
            result={"code":40000,'error': '验证码不正确!'}
            return  JsonResponse(result)
        else:
            return JsonResponse({"code":200})

@csrf_exempt
@login_check
def new_phone_view(request,username=None):
    try:
        user = User.objects.get(username=username)
    except Exception as  e:
        print('-get user error is %s-' % e)
    if request.method=='POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        phone=json_obj['phone']
        noteInput=json_obj['noteInput']
        cache_key = 'sms_%s' % phone
        a = cache.get(cache_key)
        if noteInput !=str(a):
            result={"code":40000,'error': '验证码不正确!'}
            return  JsonResponse(result)
        else:
            user.phone=phone
            user.save()
            return JsonResponse({"code":200})