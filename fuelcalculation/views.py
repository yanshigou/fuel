# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from .functions import random_str, http_response, is_user_exist
from .models import CarInfo, RefuelInfo
from .serializers import CarInfoSerializer, RefuelInfoSerializer, ExpenditureInfoSerializer, FuelInfoSerializer
import json
import requests
import traceback
from datetime import datetime


# 发送手机验证码
class SendCodeView(APIView):
    def post(self, request):
        try:
            phone = request.data.get('username')
            url = "http://023sms.cqnews.net:7891/SMSServer/smssend"
            appkey = "22687301"
            appsecret = "91VEpa8D97"
            vericode = random_str(4)
            templateid = "1519352616910Hs2"
            params = {"appkey": appkey, "appsecret": appsecret,
                      "templateid": templateid, "phone": phone, "extnum": "12345",
                      "templateparams": [vericode]}
            headers = {'content-type': 'application/json'}
            res = requests.post(url, data=json.dumps(params), headers=headers)
            code = res.json()["code"]
            msg = res.json()["msg"]
            msgid = res.json()["msgid"]
            print(code)
            if code == 0:
                wi = {"vericode": vericode, "phone": phone, "msgid": msgid, "time": datetime.now()}
                return http_response(data=wi)
            return http_response(error_no=18, info="send sms error")
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


# 车辆信息
class SetCarInfoView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            if CarInfo.objects.filter(car_id=car_id).count() > 0:
                return http_response(error_no=12, info="car_id already exist")
            car_brand = request.data.get('car_brand')
            car_name = request.data.get('car_name')
            car_series = request.data.get('car_series')
            car_model = request.data.get('car_model')
            if car_name is None:
                car_name = '我的小车'
            wi = {"username": username, "car_id": car_id, "car_brand": car_brand, "car_name": car_name,
                  "car_series": car_series, "car_model": car_model}
            ser = CarInfoSerializer(data=wi)
            if ser.is_valid():
                ser.save()
                return http_response()
            return http_response(error_no=8, info="other error ")
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def put(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            if CarInfo.objects.filter(car_id=car_id, username_id=username).count() < 1:
                return http_response(error_no=13, info="car_id not exist")
            car_brand = request.data.get('car_brand')
            car_name = request.data.get('car_name')
            car_series = request.data.get('car_series')
            car_model = request.data.get('car_model')
            if car_name is None:
                car_name = '我的小车'
            car = CarInfo.objects.get(car_id=car_id, username_id=username)
            car.car_name = car_name
            car.car_brand = car_brand
            car.car_series = car_series
            car.car_model = car_model
            car.save()
            return http_response()
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def delete(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            if CarInfo.objects.filter(car_id=car_id, username_id=username).count() < 0:
                return http_response(error_no=13, info="car_id not exist")
            CarInfo.objects.get(car_id=car_id, username_id=username).delete()
            return http_response()
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def get(self, request):
        try:
            username = request.query_params['username']
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            cars = CarInfo.objects.filter(username_id=username)
            sers = CarInfoSerializer(cars, many=True)
            return http_response(data={"cars_list": sers.data})
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


# 加油记录
class RefuelInfoView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            if CarInfo.objects.filter(car_id=car_id, username_id=username).count() < 1:
                return http_response(error_no=12, info="car_id not exist")
            is_full = request.data.get('is_full')
            is_light = request.data.get('is_light')
            is_norecord = request.data.get('is_norecord')
            fuel_type = request.data.get('fuel_type')
            mileages = request.data.get('mileages')
            prices = request.data.get('prices')
            moneys = request.data.get('moneys')
            fuel_counts = request.data.get('fuel_counts')
            fuel_station = request.data.get('fuel_station')
            remark = request.data.get('remark')
            time = request.data.get('time')
            wi = {"car_id": car_id, "is_full": is_full, "is_light": is_light, "is_norecord": is_norecord,
                  "fuel_type": fuel_type, "mileages": mileages, "prices": prices, "moneys": moneys,
                  "fuel_counts": fuel_counts, "fuel_station": fuel_station, "remark": remark, "time": time}
            ser = RefuelInfoSerializer(data=wi)
            # print(ser)
            if ser.is_valid():
                ser.save()
                return http_response()
            return http_response(error_no=8, info="other error ")
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def get(self, request):
        try:
            username = request.query_params['username']
            car_id = request.query_params['car_id']
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            refuelinfo = RefuelInfo.objects.filter(car_id=car_id)
            sers = RefuelInfoSerializer(refuelinfo, many=True)
            return http_response(data={"refuelinfo_list": sers.data})
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def put(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            id = request.data.get('id')
            if RefuelInfo.objects.filter(car_id=car_id, id=id).count() < 1:
                return http_response(error_no=13, info="refuelinfo not exist")
            is_full = request.data.get('is_full')
            is_light = request.data.get('is_light')
            is_norecord = request.data.get('is_norecord')
            fuel_type = request.data.get('fuel_type')
            mileages = request.data.get('mileages')
            prices = request.data.get('prices')
            moneys = request.data.get('moneys')
            fuel_counts = request.data.get('fuel_counts')
            fuel_station = request.data.get('fuel_station')
            remark = request.data.get('remark')
            time = request.data.get('time')
            info = RefuelInfo.objects.get(car_id=car_id, id=id)
            info.is_full = is_full
            info.is_light = is_light
            info.is_norecord = is_norecord
            info.fuel_type_id = fuel_type
            info.mileages = mileages
            info.prices = prices
            info.moneys = moneys
            info.fuel_counts = fuel_counts
            info.fuel_station = fuel_station
            info.remark = remark
            info.time = time
            info.save()
            return http_response()
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def delete(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            id = request.data.get('id')
            if RefuelInfo.objects.filter(car_id=car_id, id=id).count() < 1:
                return http_response(error_no=13, info="car_id not exist")
            RefuelInfo.objects.get(car_id=car_id, id=id).delete()
            return http_response()
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")





