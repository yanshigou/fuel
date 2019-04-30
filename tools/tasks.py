# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
from datetime import datetime
from fuelcalculation.views import RefuelInfo, RefuelInfoSerializer, FuelInfo, http_response
import traceback


@shared_task(track_started=True)
def fuel_task(car_id):
    try:
        print(car_id)
        all_refuelinfo = RefuelInfo.objects.filter(car_id=car_id).order_by('time')
        sers = RefuelInfoSerializer(all_refuelinfo, many=True)
        # 取出每次加油记录
        for i in sers.data:
            is_norecord = i.get('is_norecord')
            is_full = i.get('is_full')
            id = i.get('id')
            fuel_counts = i.get('fuel_counts')
            mileages = i.get('mileages')
            time = i.get('time')

            # 上一次有记录
            # 增加加满判断 均需两次才能计算
            if is_norecord == 0 and is_full == 1 and RefuelInfo.objects.filter(time__lt=time, car_id=car_id).count() > 0:
                last = RefuelInfo.objects.filter(time__lt=time, car_id=car_id).order_by('-time')[0]
                last_mileages = last.mileages
                last_prices = last.prices
                # 大改动——
                last_isfull = last.is_full
                last_id = last.id  # 让油耗重新赋值给上一次的记录
                last_time = last.time  # 让油耗重新赋值给上一次的记录
                if last_isfull != 1:
                    last_value = '???'
                    if FuelInfo.objects.filter(id_id=last_id, car_id_id=car_id).count() > 0:
                        f = FuelInfo.objects.get(id_id=last_id, car_id_id=car_id)
                        f.fuel_l_km = last_value
                        f.fuel_y_km = last_value
                        f.driving_km = last_value
                        f.mileages = mileages
                        f.time = last_time
                        f.driving_moneys = last_value
                        f.driving_fuel_counts = last_value
                        f.save()
                        continue
                    else:
                        FuelInfo.objects.create(id_id=last_id, car_id_id=car_id, time=last_time, fuel_l_km=last_value,
                                                fuel_y_km=last_value, mileages=mileages,
                                                driving_km=last_value,
                                                driving_moneys=last_value, driving_fuel_counts=last_value)
                        continue
                # 大改动——

                # 加满的情况下算油耗
                l = float(fuel_counts) * 100  # 使用当次加的油量
                km = int(mileages) - int(last_mileages)  # 行驶公里
                if km <= 0:
                    print(mileages, last_mileages)
                    return http_response(error_no=5, info="km error")
                # y = float(last_moneys)  # 逻辑应该为 使用金额等于上一次的单价乘以此次消耗的油量
                y = float(last_prices) * float(fuel_counts)
                fuel_l_km = float("%.2f" % (l / km))
                print("fuel_l_km:", fuel_l_km)
                fuel_y_km = float("%.2f" % (y / km))
                print("fuel_y_km", fuel_y_km)
                if FuelInfo.objects.filter(id_id=last_id, car_id_id=car_id).count() > 0:
                    f = FuelInfo.objects.get(id_id=last_id, car_id_id=car_id)
                    f.fuel_l_km = fuel_l_km
                    f.fuel_y_km = fuel_y_km
                    f.driving_km = km
                    f.mileages = last_mileages
                    f.time = last_time
                    f.driving_moneys = y
                    f.driving_fuel_counts = fuel_counts
                    f.save()
                else:
                    FuelInfo.objects.create(id_id=last_id, car_id_id=car_id, time=last_time, fuel_l_km=fuel_l_km,
                                            fuel_y_km=fuel_y_km, mileages=last_mileages, driving_km=km,
                                            driving_moneys=y, driving_fuel_counts=fuel_counts)
            elif is_full != 1:
                last_value = '???'
                last = RefuelInfo.objects.filter(time__lt=time, car_id=car_id).order_by('-time')[0]
                last_id = last.id  # 让油耗重新赋值给上一次的记录
                last_time = last.time  # 让油耗重新赋值给上一次的记录
                last_mileages = last.mileages
                if FuelInfo.objects.filter(id_id=last_id, car_id_id=car_id).count() > 0:
                    f = FuelInfo.objects.get(id_id=last_id, car_id_id=car_id)
                    f.fuel_l_km = last_value
                    f.fuel_y_km = last_value
                    f.driving_km = last_value
                    f.mileages = last_mileages
                    f.time = last_time
                    f.driving_moneys = last_value
                    f.driving_fuel_counts = last_value
                    f.save()
                else:
                    FuelInfo.objects.create(id_id=last_id, car_id_id=car_id, time=last_time, fuel_l_km=last_value,
                                            fuel_y_km=last_value, mileages=last_mileages, driving_km=last_value,
                                            driving_moneys=last_value, driving_fuel_counts=last_value)

            # 上一次没有记录
            else:
                last_value = '???'
                if FuelInfo.objects.filter(id_id=id, car_id_id=car_id).count() > 0:
                    f = FuelInfo.objects.get(id_id=id, car_id_id=car_id)
                    f.fuel_l_km = last_value
                    f.fuel_y_km = last_value
                    f.driving_km = last_value
                    f.mileages = mileages
                    f.time = time
                    f.driving_moneys = last_value
                    f.driving_fuel_counts = last_value
                    f.save()
                else:
                    FuelInfo.objects.create(id_id=id, car_id_id=car_id, time=time, fuel_l_km=last_value,
                                            fuel_y_km=last_value, mileages=mileages, driving_km=last_value,
                                            driving_moneys=last_value, driving_fuel_counts=last_value)

        # 循环后最后一次需要单独增加
        if sers.data:
            i = sers.data[-1]
            last_value = '???'
            id = i.get('id')
            mileages = i.get('mileages')
            time = i.get('time')
            if not FuelInfo.objects.filter(id_id=id, car_id_id=car_id):
                FuelInfo.objects.create(id_id=id, car_id_id=car_id, time=time, fuel_l_km=last_value,
                                        fuel_y_km=last_value, mileages=mileages, driving_km=last_value,
                                        driving_moneys=last_value, driving_fuel_counts=last_value)
        return True
    except Exception as e:
        traceback.print_exc()
        print('Exception!!', datetime.now(), e)
        return False
