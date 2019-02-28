# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2019/02/14 14:59"


from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExpenditureInfoSerializer
import random


COMMON_HEADERS = {'Access-Control-Allow-Origin': '*'}


# 检查用户是否存在
def is_user_exist(str_username):
    custom_user = UserProfile.objects.filter(username=str_username)
    if custom_user.count() > 0:
        return True
    else:
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
    print(data)
    return Response(data=data,status=status_code, headers=COMMON_HEADERS)


# 验证码
def random_str(randomlength=4):
    str = ''
    chars = '0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 记录加油费用
def refuel_moneys(car_id, moneys, remark, time, info):
    wi = {"car_id": car_id, "moneys": moneys, "remark": remark, "time": time, "info": info}
    ser = ExpenditureInfoSerializer(data=wi)
    if ser.is_valid():
        ser.save()
        return True
    return False
