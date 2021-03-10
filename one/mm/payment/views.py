from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
import json
from alipay import AliPay
from django.conf import settings

# Create your views here.
app_private_key_string=open(settings.ALIPAY_KEY_DIR+'app_private_key.pem').read()
alipay_public_key_string=open(settings.ALIPAY_KEY_DIR+'alipay_public_key.pem').read()
ORDER_STATUS=1#1待支付 2 支付成功 3支付失败
class MyAliPay(View):
    #构造函数,与支付相关参数的初始化
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #创建一个AliPay对象
        self.alipay=AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            #用户私钥
            app_private_key_string=app_private_key_string,
            #支付宝公钥
            alipay_public_key_string=alipay_public_key_string,
            #指明签名算法RAS256
            sign_type='RSA2',
            #知名为测试,请求会发送到沙箱服务器
            debug=True,
            # config=
        )
    def get_trade_url(self,order_id,amout):
        base_url='https://openapi.alipaydev.com/gateway.do'
        #构造出订单的查询字符串
        order_string=self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=amout,
            #订单标题
            subject=order_id,
            #用户支付完毕,我们告诉支付宝跳转到的商家那个页面
            return_url=settings.ALIPAY_RETURN_URL,
            #支付结果的通知url
            notify_url=settings.ALIPAY_NOTIFY_URL

        )
        return base_url+'?'+order_string
    def get_verify_result(self,data,sign):
        return self.alipay.verify(data,sign)
    def get_trade_result(self,order_id):
        result=self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get('trade_status')=="TRADE_SUCCESS":
            return True
        return False


class JumpView(MyAliPay):

    def post(self,request,money=None):
        print('进入支付宝的界面 >>>>>>>>>>>',type(money),money)
        json_obj=json.loads(request.body)
        order_id=json_obj['order_id']
        #生成一个pay_url,引导用户定向到支付宝页面
        pay_url=self.get_trade_url(order_id,money)

        return JsonResponse({'pay_url':pay_url})
class ResultView(MyAliPay):
    def get(self,request):
        # return HttpResponse('支付成功!')
        request_data={k:request.GET[k] for k in request.GET.keys()}
        # 从请求数据中取出订单编号
        order_id=request.data['out_trade_no']
        if ORDER_STATUS==2:
            return HttpResponse('支付成功')
        elif ORDER_STATUS==1:
            # 意味着接收POST请求的服务器挂啦,我们要主动查询
            result=self.get_trade_result(order_id)
            if result:
                #修改数据库的订单状态有未支付转为支付成功
                return  HttpResponse("主动查询支付成功!")
            else:
                # 修改数据库的订单状态有未支付转为支付失败
                return HttpResponse("主动查询支付失败!")

    #支付宝服务器发post请求,
    def post(self,request):
        #被动接收支付宝的支付结果通知
        #1 将POST的数据转换成字典结构
        request_data={k:request.POST[k] for k in request.POST.keys()}
        # 从中取出签名
        sign=request_data.pop('sign')
        # 验签
        is_verify=self.get_verify_result(request_data,sign)
        if is_verify:
            #从request_data取出订单状态
            trade_status=request_data['trade_status']
            if trade_status=='TRADE_SUCCESS':
                #修改数据库中的订单信息(由未支付变成支付成功)
                return HttpResponse('ok')
            else:# 修改数据库中的订单信息(由未支付变成支付失败)
                return HttpResponse('ok')

        else:

            return HttpResponse('请求不合法')