from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from login.models import User
import hashlib
from login.views import make_token


class TokenView(View):
    # @method_decorator(csrf_exempt)
    @csrf_exempt
    def post(self, request):
        print('123')
        json_str=request.body
        json_body=json.loads(json_str)
        username=json_body['username']
        password=json_body['password']
        code=json_body['code']
        codes=json_body['codes']
        a=json_body['a']
        print(username, password, code, codes, a)
        # 校验用户名和密码
        try:
            user=User.objects.get(username = username)
        except Exception as e:
            print('error is %s' % e)
            result={'code': 10200, 'error': '用户名或密码错误！'}
            return JsonResponse(result)

        md5=hashlib.md5()
        md5.update(password.encode())
        if md5.hexdigest() != user.password:
            result={'code': 10201, 'error': '用户名或密码错误！'}
            return JsonResponse(result)
        # 签发token
        token=make_token(username)
        print(token)
        token=token.decode()
        if a < 1:
            result={'code': 200, 'username': username,
                    'data': {'token': token}}
            return JsonResponse(result)
        else:
            if code != codes:
                result={'code': 10202, 'error': '验证码错误'}
                return JsonResponse(result)
            else:
                result={'code': 200, 'username': username,
                        'data': {'token': token}}
                return JsonResponse(result)
