from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
import json

from django.views.decorators.csrf import csrf_exempt

from login.models import User
import hashlib
from .tasks import send_sms
import time
import jwt
from django.conf import settings
import random
from tools.sms import YunTongXin
from tools.login_dec import login_check

class UsersView(View):
    @method_decorator(csrf_exempt)
    def get(self, request, username = None):

        if username:
            # 返回单个用户信息
            try:
                user=User.objects.get(username = username)
            except Exception as e:
                print('-get user error is %s-' % e)
                result={'code': 10104, 'error': '该用户不存在'}
                return JsonResponse(result)

            # 根据查询字符串获取指定数据
            keys=request.GET.keys()
            if keys:
                data={}
                for k in keys:
                    if k == 'password':
                        continue
                    if hasattr(user, k):
                        data[k]=getattr(user, k)
                result={'code': 200, 'username': username,
                        'data': data}
            else:
                # 获取用户的全量数据
                result={'code': 200, 'username': username,
                        'data': {
                            'info': user.info, 'sign': user.sign,
                            'nickname': user.nickname,
                            'avatar': str(user.avatar)}}
            return JsonResponse(result)


        else:
            # 返回所有用户信息
            pass
        return HttpResponse('--users get--')

    @method_decorator(csrf_exempt)
    def post(self, request):
        json_str=request.body
        json_obj=json.loads(json_str)
        username=json_obj['username']
        postbox=json_obj['postbox']
        tem=json_obj['tem']
        password_1=json_obj['password_1']
        password=json_obj['password']
        key=json_obj['key']
        question=json_obj['question']
        check=json_obj['check']
        sum=json_obj['sum']
        print(username, postbox, tem, password_1, password, key, question, check, sum)

        # 1 用户名长度检查
        if len(username) > 11:
            result={'code': 10100, 'error': '用户名太长！'}
            return JsonResponse(result)
        if not username or not password or not password_1:
            result={'code': 10104, 'error': '用户名或者密码不能为空'}
            return JsonResponse(result)
        if not key:
            result={'code': 10105, 'error': '答案不能为空'}
            return JsonResponse(result)
        a=cache.get('sms_%s' % tem)
        if int(sum) != a:
            result={'code': 10106, 'error': '验证码错误'}
            return JsonResponse(result)
        if check == False:
            result={'code': 10108, 'error': '未同意版权声明'}
            return JsonResponse(result)
        # 2 用户名是否可用
        old_user=User.objects.filter(username = username)
        if old_user:
            result={'code': 10101, 'error': '用户名已被占用！'}
            return JsonResponse(result)
        old_nickname = User.objects.filter(nickname=username)
        if old_nickname:
            result = {'code': 50102, 'error': '用户名已被占用!'}
            return JsonResponse(result)
        # 3 两次密码要一致
        if question == '请选择密保问题':
            result={'code': 10103, 'error': '密保问题未选择'}
            return JsonResponse(result)

        if password_1 != password:
            result={'code': 10102, 'error': '两次密码不一致！'}
            return JsonResponse(result)
        # 4 hash处理
        md5=hashlib.md5()
        md5.update(password_1.encode())
        password_h=md5.hexdigest()
        # 5 添加到数据库
        try:
            user=User.objects.create(username = username,
                                     password = password_h,
                                     email = postbox,
                                     phone = tem,
                                     nickname = username,
                                     problem = question,
                                     key = key)
        except Exception as e:
            print('create error is %s' % e)
            result={'code': 10103, 'error': '用户名被占用！'}
            return JsonResponse(result)
        # 签发token
        token=make_token(username)
        # 字节串表示的token转换为字符串
        token=token.decode()

        # res.data.token
        return JsonResponse({'code': 200, 'username': username,
                             'data': {'token': token}})

@csrf_exempt
def make_token(username, expire = 3600 * 24):
    key=settings.JWT_TOKEN_KEY
    now=time.time()
    payload={'username': username, 'exp': now + expire}
    return jwt.encode(payload, key, algorithm = 'HS256')

@csrf_exempt
def sms_view(request):
    json_str=request.body
    json_obj=json.loads(json_str)
    # 获取用户输入的手机号
    phone=json_obj['phone']

    # 生成键
    cache_key='sms_%s' % phone

    # 生成随机的验证码
    code=random.randint(1000, 9999)
    # 存储到哪儿？键？
    cache.set(cache_key, code, 180)
    a=cache.get(cache_key)
    print('--send code %s--' % code)
    print(cache_key)
    # # 创建容联云对象
    # x = YunTongXin(settings.SMS_ACCOUNT_ID, settings.SMS_ACCOUNT_TOKEN,
    #                settings.SMS_APP_ID, settings.SMS_TEMPLATE_ID)
    # # 发送短信
    # res = x.run(phone, code)
    # print('--send sms result is %s--' % res)
    # return JsonResponse({'code': 200})
    res=send_sms.delay(phone, code)
    print('--send sms result is %s--' % res)
    return JsonResponse({'code': 200})
