# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
import traceback
from datetime import datetime, timedelta
import time
import random
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import base64
import json
from urllib import urlencode
from django.http import HttpResponse
import re
from fuelcalculation.models import OrderInfo
from fuelcalculation.userviews import is_user_exist


# ali_appid = "2019032863742360"
ali_appid = "2016092700609405"  # 沙箱
method = "alipay.trade.precreate"
unified_url = "https://openapi.alipaydev.com/gateway.do"
notify_url = "http://www.dogebug.online:9000/alipay/payresult/"
COMMON_HEADERS = {'Access-Control-Allow-Origin': '*'}


class AliUnifiedPayViewSet(APIView):
    def post(self, request):
        try:
            print_log("post alipay/unifiedpay/")
            username = request.data.get("username")
            if not is_user_exist(username):
                return http_response(error_no=42, info="no this user")
            total_fee = request.data.get("total_fee")
            body = request.data.get('body')
            out_trade_no = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            out_trade_no += random_str()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            total_amount = str('%.2f' % (float(total_fee)/100))
            print(total_amount)
            wait_data = {
                "app_id": ali_appid,
                "method": method,
                "format": "json",
                "charset": 'utf-8',
                "sign_type": "RSA2",
                "timestamp": timestamp,
                "version": "1.0",
                "notify_url": notify_url,
                "biz_content": {
                    "body": body,
                    "subject": body,
                    "out_trade_no": out_trade_no,
                    "total_amount": str(total_amount)
                }
            }
            # print(wait_data)
            unsigned_items = ordered_data(wait_data)
            # 未签名字符串
            unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
            # print(unsigned_string)
            # 签名字符串
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            private_path = os.path.join(BASE_DIR, 'static') + '\\rsa_private_key.pem'
            public_path = os.path.join(BASE_DIR, 'static') + '\\alipay_public_key.pem'
            if os.path.exists(private_path) and os.path.exists(public_path):
                print(private_path)
                print(public_path)
            else:
                private_path = '/home/database/yinxuan/chengdu/static/rsa_private_key.pem'
                public_path = '/home/database/yinxuan/chengdu/static/alipay_public_key.pem'

                # private_path = 'G:\\dzt\\Work_CMX\\project\\chengdu\\static\\rsa_private_key.pem'
                # public_path = 'G:\\dzt\\Work_CMX\\project\\chengdu\\static\\alipay_public_key.pem'

            signed_string = sign_string(private_path, unsigned_string)
            print(signed_string)
            # # 验签
            # result = validate_sign("G:\\dzt\\Work_CMX\\project\\chengdu\\static\\rsa_public_key.pem", unsigned_string,
            #                        signed_string)
            data = {
                "app_id": ali_appid,
                "method": method,
                "charset": 'utf-8',
                "format": "json",
                "sign_type": "RSA2",
                "timestamp": timestamp,
                "version": "1.0",
                "notify_url": notify_url,
                "biz_content": {
                    "body": body,
                    "subject": body,
                    "out_trade_no": out_trade_no,
                    "total_amount": str(total_amount)
                },
                "sign": signed_string
            }
            # print(urlencode(data))
            # 进行排序和去除空值去除空格 不然urlencode的值会出问题
            unsigned_items = ordered_data(data)
            # print(urlencode(data))
            # print(unsigned_items)
            url = unified_url + "?" + urlencode(data)
            res = requests.get(url)
            # print(url)
            res_json = json.loads(res.content)
            alipay_trade_precreate_response = res_json.get('alipay_trade_precreate_response')
            print(res.content)
            unvalidate_sign = re.findall('{"code":.*"},', res.content)
            print(unvalidate_sign)
            # alipay_unsigned_items = ordered_data(res_json)
            # alipay_unsigned_string = "&".join("{}={}".format(k, v) for k, v in alipay_unsigned_items)
            # print(alipay_unsigned_string)
            alipay_code = alipay_trade_precreate_response.get('code')
            alipay_msg = alipay_trade_precreate_response.get('msg')
            alipay_out_trade_no = alipay_trade_precreate_response.get('out_trade_no')
            alipay_qr_code = alipay_trade_precreate_response.get('qr_code')
            alipay_sign = res_json.get('sign')
            if alipay_code == "10000" and alipay_msg == 'Success':
                # 同步验签
                result = validate_sign(public_path, unvalidate_sign[0][:-1], alipay_sign)
                if result:
                    OrderInfo.objects.create(ordernum=out_trade_no, orderuser_id=username,
                                             ordermoney=total_fee, order_paytype=2,
                                             ordertime=datetime.now())
                    return http_response(data={"alipay_qr_code": alipay_qr_code,
                                               "alipay_out_trade_no": alipay_out_trade_no})
                return http_response(error_no=99, info="yanqian shibai")
            return http_response(error_no=98, info="chuangjiandingdan shibai")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


class AliPayResultViewSet(APIView):
    def post(self, request):
        try:
            print_log("post alipay/payresult/")
            print(request.data)
            app_id = request.data.get('app_id')
            print(app_id)
            sign_type = request.data.get('sign_type')
            if app_id == ali_appid and sign_type == 'RSA2':
                pass
            sign = request.data.get('sign')
            trade_no = request.data.get('trade_no')
            print(sign)
            print(trade_no)
            out_trade_no = request.data.get('out_trade_no')
            print(out_trade_no)
            trade_status = request.data.get('trade_status')
            gmt_create = request.data.get('gmt_create')
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            public_path = os.path.join(BASE_DIR, 'static') + '\\alipay_public_key.pem'
            if os.path.exists(public_path):
                print(public_path)
            else:
                public_path = '/home/database/yinxuan/chengdu/static/alipay_public_key.pem'
            params = request.data.dict()
            sign = params.pop('sign', None)  # 取出签名
            params.pop('sign_type')  # 去出签名类型
            unsigned_items = ordered_data(params)
            # 未签名字符串
            unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
            result = validate_sign(public_path, unsigned_string, sign)
            if not result:
                print('yanqian shibai')
                return http_response(error_no=99, info="yanqian shibai")
            if OrderInfo.objects.filter(ordernum=out_trade_no, order_paytype=2).count() > 0:
                orderinfos = OrderInfo.objects.get(ordernum=out_trade_no, order_paytype=2)
                # 如果订单支付完成已经回调过
                if trade_status == "WAIT_BUYER_PAY" and orderinfos.orderstatus == 0:
                    orderinfos.order_paynum = trade_no
                    orderinfos.ordertime = gmt_create
                    orderinfos.save()
                elif trade_status == ("TRADE_SUCCESS" or "TRADE_FINISHED") and orderinfos.orderstatus == 0:
                    orderinfos.orderstatus = 1
                    orderinfos.save()
                    print("success")
                    return HttpResponse("success")
                elif trade_status == "TRADE_SUCCESS" and orderinfos.orderstatus == 1:
                    print("success")
                    return HttpResponse("success")
            return HttpResponse("success")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据单独排序
    for key in complex_keys:
        data[key] = json.dumps(data[key], sort_keys=True).replace(" ", "")

    return sorted([(k, v) for k, v in data.items()])


# RSA(SHA256)签名
def sign_string(private_key_path, unsigned_string):
    # 开始计算签名
    key = RSA.importKey(open(private_key_path).read())
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(unsigned_string.encode("utf8")))
    # base64 编码，转换为unicode表示并移除回车
    sign = base64.encodestring(signature).decode("utf8").replace("\n", "")
    return sign


# 验签
def validate_sign(public_key_path, message, signature):
    # 开始计算签名
    key = RSA.importKey(open(public_key_path).read())
    signer = PKCS1_v1_5.new(key)
    digest = SHA256.new()
    digest.update(message.encode("utf8"))
    if signer.verify(digest, base64.decodestring(signature.encode("utf8"))):
        return True
    return False


def http_response(data=None, error_no=None, info=None, status_code=None, imei=None):
    if status_code == None:
        status_code = status.HTTP_200_OK
    if error_no==None:
        error_no = 0
    if info == None:
        info = "Success"
    if data==None:
        data={}
    data["error"] = info
    data["error_no"] = error_no
    if imei != None:
        data["imei"] = imei
    print data
    return Response(data=data, status=status_code, headers=COMMON_HEADERS)


def random_str(randomlength=4):
    str = ''
    chars = '0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def print_log(info):
    print(" ")
    print(datetime.now())
    print(info)
