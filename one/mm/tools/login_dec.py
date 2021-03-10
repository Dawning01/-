from django.http import JsonResponse
import jwt
from django.conf import settings
from login.models import User


def login_check(func):
    print('#################在进入装饰器前Put ############################')
    def wrap(request,*args,**kwargs):
    # 从请求头中获取token
        token=request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result={'code':403,'error':'请登录'}
            return JsonResponse(result)
        # 校验token
        try:
            payload=jwt.decode(token,settings.JWT_TOKEN_KEY,
                       algorithms='HS256'
                       )
        except Exception as e:
            print('check login error %s'%e)
            result = {'code': 403, 'error': '请登录'}
            return JsonResponse(result)
        # 从载荷中获取私声明
        username=payload['username']
        # 根据用户名称获取用户对象
        user=User.objects.get(username=username)
        print(user)
        #将用户对象保存到request对象中
        request.myuser=user

        print('#################在离开装饰器前Put ############################')
        return func(request,*args,**kwargs)
    return wrap
def get_user_by_request(request):
    token=request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try :
        res=jwt.decode(token,settings.JWT_TOKEN_KEY)
    except Exception as e:
        print('get user jwt is error %s'%e)
        return None
    username=res['username']
    return username