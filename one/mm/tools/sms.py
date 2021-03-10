import datetime
import hashlib
import base64
import json

import requests  # 使用它可以发送http/https请求
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class YunTongXin():

    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId


    # 1 构造url
    def get_request_url(self, sig):
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sig)
        return self.url

    # 时间戳
    def get_timestamp(self):
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S")
        return now_str

    # 计算sig参数
    def get_sig(self, timestamp):
        s = self.accountSid + self.accountToken + timestamp
        md5 = hashlib.md5()
        md5.update(s.encode())
        return md5.hexdigest().upper()

    # 2 构造包头
    def get_request_header(self, timestamp):
        s = self.accountSid + ':' + timestamp
        # 1. s.encode(),将参数由字符串转换成字节串
        # 2. b64encode做base64编码
        # 3. 最后的decode()将计算结果由字节串转换为字符串
        b_s = base64.b64encode(s.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': b_s
        }

    # 3 构造请求体
    def get_request_body(self, phone, code):
        data = {
            'to': phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, '3']
        }
        return data

    # 4 发送请求
    def do_request(self, url, header, body):
        # 1. url:post请求发给哪个资源
        # 2. headers 请求头
        # 3. body 请求体
        res = requests.post(url=url, headers=header,
                            data=json.dumps(body))
        return res.text

    # 5 运行(将以上几步串起来)
    def run(self, phone, code):
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)
        print(url)
        header = self.get_request_header(timestamp)
        print(header)
        body = self.get_request_body(phone, code)
        print(body)
        res = self.do_request(url, header, body)
        return res


if __name__ == '__main__':
    aid = "8aaf070877807ed80177b3e0e38806a1"
    atoken = "4454986107104661be11cce546dfba58"
    appid = "8aaf070877807ed80177b3e0e44806a7"
    tid = "1"

    x = YunTongXin(aid, atoken, appid, tid)
    res = x.run('18372689867', '123456')
    print(res)
