from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from login.models import User

class Change(View):
    def get(self, request, username = None):
       if username:
           try:
               user=User.objects.get(username = username)
           except Exception as e:
               print('-get user error is %s-' % e)
               result={'code': 10104, 'error': '该用户不存在'}
               return JsonResponse(result)
       nickname=user.nickname
       if user.vip==0:
           vip="普通用户"

       else:
           vip="普通会员"

       # print(f'##########会员vip:{vip}#####################')
       created_time=user.created_time.strftime('%Y-%m-%d')
       data={'code':200,"data":{"nickname":nickname,"vip":vip,"created_time":created_time}}
       print({"nickname":nickname,"vip":vip,"created_time":created_time})
       return JsonResponse(data)