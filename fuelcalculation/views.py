# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from .functions import random_str, http_response, is_user_exist, refuel_moneys
from .models import CarInfo, RefuelInfo, FuelInfo, RankingList, ExpenditureInfo, CarCareInfo
from .serializers import CarInfoSerializer, RefuelInfoSerializer, ExpenditureInfoSerializer, FuelInfoSerializer
from .serializers import RankingListSerializer, CarCareInfoSerializer
import json
import requests
import traceback
from datetime import datetime, timedelta


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


# TODO 开一个或多个接口提供品牌、车系、车型数据


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
            username = request.query_params.get('username')
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
                if refuel_moneys(car_id, moneys, remark, time, "加油"):
                    return http_response()
                return http_response(info="refuel_moneys error")
            return http_response(error_no=8, info="sers error ")
        except KeyError:
            return http_response(error_no=1, info="input error")
        except ZeroDivisionError:
            return http_response(error_no=1, info="integer division or modulo by zero")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def get(self, request):
        try:
            username = request.query_params.get('username')
            car_id = request.query_params.get('car_id')
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


# 油耗
class FuelCalculationView(APIView):
    def get(self, request):
        try:
            username = request.query_params.get("username")
            car_id = request.query_params.get('car_id')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            all_refuelinfo = RefuelInfo.objects.filter(car_id=car_id)
            sers = RefuelInfoSerializer(all_refuelinfo, many=True)
            # 取出每次加油记录
            for i in sers.data:
                is_norecord = i.get('is_norecord')
                id = i.get('id')
                fuel_counts = i.get('fuel_counts')
                mileages = i.get('mileages')
                moneys = i.get('moneys')
                time = i.get('time')

                # 上一次有记录
                if is_norecord == 0 and RefuelInfo.objects.filter(time__lt=time, car_id=car_id).count() > 0:
                    last = RefuelInfo.objects.filter(time__lt=time, car_id=car_id).order_by('-time')[0]
                    last_mileages = last.mileages
                    l = float(fuel_counts) * 100
                    km = int(mileages) - int(last_mileages)
                    if km <= 0:
                        print(mileages, last_mileages)
                        return http_response(error_no=5, info="km error")
                    y = float(moneys)
                    fuel_l_km = float("%.2f" % (l / km))
                    print("fuel_l_km:", fuel_l_km)
                    fuel_y_km = float("%.2f" % (y / km))
                    print("fuel_y_km", fuel_y_km)
                    if FuelInfo.objects.filter(id_id=id, car_id_id=car_id).count() > 0:
                        f = FuelInfo.objects.get(id_id=id, car_id_id=car_id)
                        f.fuel_l_km = fuel_l_km
                        f.fuel_y_km = fuel_y_km
                        f.driving_km = km
                        f.mileages = mileages
                        f.time = time
                        f.driving_moneys = y
                        f.driving_fuel_counts = fuel_counts
                        f.save()
                    else:
                        FuelInfo.objects.create(id_id=id, car_id_id=car_id, time=time, fuel_l_km=fuel_l_km,
                                                fuel_y_km=fuel_y_km, mileages=mileages, driving_km=km,
                                                driving_moneys=moneys, driving_fuel_counts=fuel_counts)
                # 上一次没有记录
                else:
                    last_mileages = '???'
                    if FuelInfo.objects.filter(id_id=id, car_id_id=car_id).count() > 0:
                        f = FuelInfo.objects.get(id_id=id, car_id_id=car_id)
                        f.fuel_l_km = last_mileages
                        f.fuel_y_km = last_mileages
                        f.driving_km = last_mileages
                        f.mileages = mileages
                        f.time = time
                        f.save()
                    else:
                        FuelInfo.objects.create(id_id=id, car_id_id=car_id, time=time, fuel_l_km=last_mileages,
                                                fuel_y_km=last_mileages, mileages=mileages, driving_km=last_mileages,
                                                driving_moneys=moneys, driving_fuel_counts=fuel_counts)

            all_fuelinfo = FuelInfo.objects.filter(car_id_id=car_id)
            sers = FuelInfoSerializer(all_fuelinfo, many=True)
            return http_response(data={"all_fuelinfo": sers.data})
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


# 排行榜
class RankingListView(APIView):
    def get(self, request):
        try:
            username = request.query_params.get("username")
            car_id = request.query_params.get('car_id')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            all_fuelinfo = FuelInfo.objects.filter(car_id=car_id)
            if all_fuelinfo.count() < 1:
                return http_response(error_no=42, info="No car_id")
            sers = FuelInfoSerializer(all_fuelinfo, many=True)
            # 取出油耗记录
            list_time = []
            list_fuel_l_km = []
            list_fuel_y_km = []
            list_mileages = []
            list_driving_km = []
            list_driving_moneys = []
            list_driving_fuel_counts = []
            for i in sers.data:
                fuel_l_km = i.get('fuel_l_km')
                if fuel_l_km == ('???' or '?'):
                    continue
                time = i.get('time')
                fuel_y_km = i.get('fuel_y_km')
                mileages = i.get('mileages')
                driving_km = i.get('driving_km')
                driving_moneys = i.get('driving_moneys')
                driving_fuel_counts = i.get('driving_fuel_counts')
                list_time.append(time)
                list_fuel_l_km.append(float(fuel_l_km))
                list_fuel_y_km.append(float(fuel_y_km))
                list_mileages.append(int(mileages))
                list_driving_km.append(int(driving_km))
                list_driving_moneys.append(float(driving_moneys))
                list_driving_fuel_counts.append(float(driving_fuel_counts))
            average_fuel_l_km = sum(list_fuel_l_km) / len(list_fuel_l_km)
            average_fuel_y_km = sum(list_fuel_y_km) / len(list_fuel_y_km)
            km = max(list_mileages)
            sum_km = sum(list_driving_km)
            sum_moneys = sum(list_driving_moneys)
            sum_fuel_counts = sum(list_driving_fuel_counts)
            if RankingList.objects.filter(car_id=car_id).count() > 0:
                rank = RankingList.objects.get(car_id=car_id)
                rank.average_fuel_l_km = average_fuel_l_km
                rank.average_fuel_y_km = average_fuel_y_km
                rank.km = rank.km
                rank.sum_km = sum_km
                rank.sum_moneys = sum_moneys
                rank.sum_fuel_counts = sum_fuel_counts
                rank.save()
                # sers = RankingListSerializer(rank)
                # return http_response(data={"ranklist": sers.data})
            else:
                wi = {"average_fuel_l_km": average_fuel_l_km, "average_fuel_y_km": average_fuel_y_km, "km": km,
                      "sum_km": sum_km, "sum_moneys": sum_moneys, "sum_fuel_counts": sum_fuel_counts,
                      "car_id": car_id, "username": username}
                sers = RankingListSerializer(data=wi)
                if sers.is_valid():
                    sers.save()
                #     return http_response(data={"ranklist": sers.data})
                # return http_response(error_no=8, info="other error ")
            all = RankingList.objects.all().order_by('average_fuel_l_km')[:10]
            all_rank = RankingListSerializer(all, many=True)
            return http_response(data={"ranklist": all_rank.data})
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


# 支出费用
class ExpenditureInfoView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            if CarInfo.objects.filter(car_id=car_id, username_id=username).count() < 1:
                return http_response(error_no=12, info="car_id not exist")
            remark = request.data.get('remark')
            moneys = request.data.get('moneys')
            time = request.data.get('time')
            info = request.data.get('info')
            if refuel_moneys(car_id, moneys, remark, time, info):
                return http_response()
            # wi = {"car_id": car_id, "moneys": moneys, "remark": remark, "time": time, "info": info}
            # ser = ExpenditureInfoSerializer(data=wi)
            # if ser.is_valid():
            #     ser.save()
            return http_response(error_no=8, info="other error ")
        except KeyError:
            return http_response(error_no=1, info="input error")
        except ZeroDivisionError:
            return http_response(error_no=1, info="integer division or modulo by zero")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def get(self, request):
        try:
            username = request.query_params.get('username')
            car_id = request.query_params.get('car_id')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            refuelinfo = ExpenditureInfo.objects.filter(car_id=car_id)
            sers = ExpenditureInfoSerializer(refuelinfo, many=True)
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
            if ExpenditureInfo.objects.filter(car_id=car_id, id=id).count() < 1:
                return http_response(error_no=13, info="ExpenditureInfo not exist")
            moneys = request.data.get('moneys')
            remark = request.data.get('remark')
            time = request.data.get('time')
            info = request.data.get('info')
            Einfo = ExpenditureInfo.objects.get(car_id=car_id, id=id)
            Einfo.moneys = moneys
            Einfo.info = info
            Einfo.time = time
            Einfo.remark = remark
            Einfo.save()
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
            if ExpenditureInfo.objects.filter(car_id=car_id, id=id).count() < 1:
                return http_response(error_no=13, info="ExpenditureInfo not exist")
            ExpenditureInfo.objects.get(car_id=car_id, id=id).delete()
            return http_response()
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


# 保养记录
class CarCareInfoView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            car_id = request.data.get('car_id')
            if CarInfo.objects.filter(car_id=car_id, username_id=username).count() < 1:
                return http_response(error_no=12, info="car_id not exist")
            time = str(request.data.get('time'))
            km = str(request.data.get('km'))
            care_type = request.data.get('care_type')
            moneys = request.data.get('moneys')
            remark = request.data.get('remark')
            # 判断保养类型 下一次保养时间和公里对应加上
            if CarCareInfo.objects.filter(car_id_id=car_id, time=time, care_type=care_type):
                return http_response(error_no=10, info="already exist")
            if care_type == 0:
                days = 182
                next_km = int(km) + 5000
                next_time = datetime.strptime(time, '%Y-%m-%d %H:%M') + timedelta(days=days)
                CarCareInfo.objects.create(car_id_id=car_id, time=time, km=km, care_type=care_type, next_km=next_km,
                                           next_time=next_time, remark=remark)
            elif care_type == 1:
                days = 2 * 365
                next_km = int(km) + 40000
                next_time = datetime.strptime(time, '%Y-%m-%d %H:%M') + timedelta(days=days)
                CarCareInfo.objects.create(car_id_id=car_id, time=time, km=km, care_type=care_type, next_km=next_km,
                                           next_time=next_time, remark=remark)
            elif care_type == 2:
                days = 5 * 365
                next_km = int(km) + 100000
                next_time = datetime.strptime(time, '%Y-%m-%d %H:%M') + timedelta(days=days)
                CarCareInfo.objects.create(car_id_id=car_id, time=time, km=km, care_type=care_type, next_km=next_km,
                                           next_time=next_time, remark=remark)
            else:
                return http_response(error_no=9, info='type error')
            if refuel_moneys(car_id, moneys, remark, time, care_type):
                carCareInfo = CarCareInfo.objects.get(car_id_id=car_id, time=time, care_type=care_type)
                sers = CarCareInfoSerializer(carCareInfo)
                return http_response(data={"data": sers.data})
            return http_response(error_no=8, info="other error ")
        except KeyError:
            return http_response(error_no=1, info="input error")
        except ZeroDivisionError:
            return http_response(error_no=1, info="integer division or modulo by zero")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def get(self, request):
        try:
            username = request.query_params.get('username')
            car_id = request.query_params.get('car_id')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            carCareInfo = CarCareInfo.objects.filter(car_id_id=car_id)
            sers = CarCareInfoSerializer(carCareInfo, many=True)
            return http_response(data={"data": sers.data})
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
            if CarCareInfo.objects.filter(car_id_id=car_id, id=id).count() < 1:
                return http_response(error_no=13, info="CarCareInfo not exist")
            time = request.data.get('time')
            km = request.data.get('km')
            care_type = request.data.get('care_type')
            next_time = request.data.get('next_time')
            next_km = request.data.get('next_km')
            remark = request.data.get('remark')
            info = CarCareInfo.objects.get(car_id=car_id, id=id)
            info.time = time
            info.km = km
            info.care_type = care_type
            info.next_time = next_time
            info.next_km = next_km
            info.remark = remark
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
            if CarCareInfo.objects.filter(car_id_id=car_id, id=id).count() < 1:
                return http_response(error_no=13, info="CarCareInfo not exist")
            CarCareInfo.objects.get(car_id=car_id, id=id).delete()
            return http_response()
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


# TODO 油价查询 聚合数据
# http://apis.juhe.cn/cnoil/oil_city
# 请求地址：http://apis.juhe.cn/cnoil/oil_city
# 请求参数：dtype=&key=81494dec79533d4cff679d470b4daa97
# 请求方式：GET
"""
{
	"resultcode":"200",
	"reason":"查询成功!",
	"result":[
		{
			"city":"北京",
			"b90":"-",
			"b93":"6.87",
			"b97":"7.31",
			"b0":"6.54",
			"92h":"6.87",
			"95h":"7.31",
			"98h":"8.29",
			"0h":"6.54"
		},
		{
			"city":"上海",
			"b90":"-",
			"b93":"6.83",
			"b97":"7.27",
			"b0":"6.48",
			"92h":"6.83",
			"95h":"7.27",
			"98h":"8.02",
			"0h":"6.48"
		},
		{
			"city":"江苏",
			"b90":"-",
			"b93":"6.84",
			"b97":"7.28",
			"b0":"6.47",
			"92h":"6.84",
			"95h":"7.28",
			"98h":"8.16",
			"0h":"6.47"
		},
		{
			"city":"天津",
			"b90":"-",
			"b93":"6.86",
			"b97":"7.24",
			"b0":"6.50",
			"92h":"6.86",
			"95h":"7.24",
			"98h":"8.16",
			"0h":"6.50"
		},
		{
			"city":"重庆",
			"b90":"-",
			"b93":"6.94",
			"b97":"7.33",
			"b0":"6.58",
			"92h":"6.94",
			"95h":"7.33",
			"98h":"8.26",
			"0h":"6.58"
		},
		{
			"city":"江西",
			"b90":"-",
			"b93":"6.83",
			"b97":"7.33",
			"b0":"6.55",
			"92h":"6.83",
			"95h":"7.33",
			"98h":"8.33",
			"0h":"6.55"
		},
		{
			"city":"辽宁",
			"b90":"-",
			"b93":"6.84",
			"b97":"7.29",
			"b0":"6.42",
			"92h":"6.84",
			"95h":"7.29",
			"98h":"7.94",
			"0h":"6.42"
		},
		{
			"city":"安徽",
			"b90":"-",
			"b93":"6.83",
			"b97":"7.32",
			"b0":"6.54",
			"92h":"6.83",
			"95h":"7.32",
			"98h":"8.15",
			"0h":"6.54"
		},
		{
			"city":"内蒙古",
			"b90":"-",
			"b93":"6.82",
			"b97":"7.32",
			"b0":"6.33",
			"92h":"6.82",
			"95h":"7.32",
			"98h":"8.05",
			"0h":"6.33"
		},
		{
			"city":"福建",
			"b90":"-",
			"b93":"6.84",
			"b97":"7.30",
			"b0":"6.50",
			"92h":"6.84",
			"95h":"7.30",
			"98h":"7.99",
			"0h":"6.50"
		},
		{
			"city":"宁夏",
			"b90":"-",
			"b93":"6.78",
			"b97":"7.16",
			"b0":"6.40",
			"92h":"6.78",
			"95h":"7.16",
			"98h":"8.20",
			"0h":"6.40"
		},
		{
			"city":"甘肃",
			"b90":"-",
			"b93":"6.76",
			"b97":"7.22",
			"b0":"6.40",
			"92h":"6.76",
			"95h":"7.22",
			"98h":"7.68",
			"0h":"6.40"
		},
		{
			"city":"青海",
			"b90":"-",
			"b93":"6.82",
			"b97":"7.31",
			"b0":"6.43",
			"92h":"6.82",
			"95h":"7.31",
			"98h":"0",
			"0h":"6.43"
		},
		{
			"city":"广东",
			"b90":"-",
			"b93":"6.89",
			"b97":"7.46",
			"b0":"6.51",
			"92h":"6.89",
			"95h":"7.46",
			"98h":"7.99",
			"0h":"6.51"
		},
		{
			"city":"山东",
			"b90":"-",
			"b93":"6.85",
			"b97":"7.34",
			"b0":"6.50",
			"92h":"6.85",
			"95h":"7.34",
			"98h":"8.06",
			"0h":"6.50"
		},
		{
			"city":"广西",
			"b90":"-",
			"b93":"6.93",
			"b97":"7.48",
			"b0":"6.56",
			"92h":"6.93",
			"95h":"7.48",
			"98h":"8.25",
			"0h":"6.56"
		},
		{
			"city":"山西",
			"b90":"-",
			"b93":"6.82",
			"b97":"7.36",
			"b0":"6.56",
			"92h":"6.82",
			"95h":"7.36",
			"98h":"8.06",
			"0h":"6.56"
		},
		{
			"city":"贵州",
			"b90":"-",
			"b93":"6.99",
			"b97":"7.39",
			"b0":"6.61",
			"92h":"6.99",
			"95h":"7.39",
			"98h":"8.29",
			"0h":"6.61"
		},
		{
			"city":"陕西",
			"b90":"-",
			"b93":"6.76",
			"b97":"7.14",
			"b0":"6.40",
			"92h":"6.76",
			"95h":"7.14",
			"98h":"7.98",
			"0h":"6.40"
		},
		{
			"city":"海南",
			"b90":"-",
			"b93":"7.98",
			"b97":"8.47",
			"b0":"6.59",
			"92h":"7.98",
			"95h":"8.47",
			"98h":"9.57",
			"0h":"6.59"
		},
		{
			"city":"四川",
			"b90":"-",
			"b93":"6.90",
			"b97":"7.43",
			"b0":"6.60",
			"92h":"6.90",
			"95h":"7.43",
			"98h":"8.09",
			"0h":"6.60"
		},
		{
			"city":"河北",
			"b90":"-",
			"b93":"6.86",
			"b97":"7.24",
			"b0":"6.50",
			"92h":"6.86",
			"95h":"7.24",
			"98h":"8.06",
			"0h":"6.50"
		},
		{
			"city":"西藏",
			"b90":"-",
			"b93":"7.75",
			"b97":"8.20",
			"b0":"7.06",
			"92h":"7.75",
			"95h":"8.20",
			"98h":"0",
			"0h":"7.06"
		},
		{
			"city":"河南",
			"b90":"-",
			"b93":"6.87",
			"b97":"7.34",
			"b0":"6.49",
			"92h":"6.87",
			"95h":"7.34",
			"98h":"7.99",
			"0h":"6.49"
		},
		{
			"city":"新疆",
			"b90":"-",
			"b93":"6.77",
			"b97":"7.27",
			"b0":"6.39",
			"92h":"6.77",
			"95h":"7.27",
			"98h":"8.12",
			"0h":"6.39"
		},
		{
			"city":"黑龙江",
			"b90":"-",
			"b93":"6.86",
			"b97":"7.36",
			"b0":"6.34",
			"92h":"6.86",
			"95h":"7.36",
			"98h":"8.39",
			"0h":"6.34"
		},
		{
			"city":"吉林",
			"b90":"-",
			"b93":"6.83",
			"b97":"7.37",
			"b0":"6.42",
			"92h":"6.83",
			"95h":"7.37",
			"98h":"8.03",
			"0h":"6.42"
		},
		{
			"city":"云南",
			"b90":"-",
			"b93":"7.01",
			"b97":"7.52",
			"b0":"6.58",
			"92h":"7.01",
			"95h":"7.52",
			"98h":"8.20",
			"0h":"6.58"
		},
		{
			"city":"湖北",
			"b90":"-",
			"b93":"6.87",
			"b97":"7.36",
			"b0":"6.49",
			"92h":"6.87",
			"95h":"7.36",
			"98h":"7.95",
			"0h":"6.49"
		},
		{
			"city":"浙江",
			"b90":"-",
			"b93":"6.84",
			"b97":"7.28",
			"b0":"6.49",
			"92h":"6.84",
			"95h":"7.28",
			"98h":"7.97",
			"0h":"6.49"
		},
		{
			"city":"湖南",
			"b90":"-",
			"b93":"6.82",
			"b97":"7.25",
			"b0":"6.57",
			"92h":"6.82",
			"95h":"7.25",
			"98h":"8.05",
			"0h":"6.57"
		}
	],
	"error_code":0
}
"""