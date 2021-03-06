# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2019/4/18"


import requests
import json
from time import sleep
from datetime import datetime
import traceback

headers = {'content-type': 'application/json'}


def import_brand():
    f = open("CarInfo.txt")
    lines = f.readlines()

    l = []
    for line in lines:
        try:
            car_brand = line.replace('\n', '').split(" ")[0].decode('utf-8')
            print(car_brand)
            if car_brand in l:
                continue
            l.append(car_brand)
            body = {
                "car_brand": car_brand
            }
            res = requests.post("http://www.dogebug.online:9000/fuelcal/carBrand/", data=json.dumps(body), headers=headers)
            print(res)
        except:
            traceback.print_exc()
            sleep(1)
            pass
    f.close()
    print(len(l))


def import_series():
    f = open("CarInfo.txt")
    lines = f.readlines()

    l = []
    for line in lines:
        try:
            car_brand = line.replace('\n', '').split(" ")[0].decode('utf-8')
            car_series = line.replace('\n', '').split(" ")[1].decode('utf-8')
            print(car_series)
            if car_series in l:
                continue
            l.append(car_series)
            body = {
                "car_brand": car_brand,
                "car_series": car_series
            }
            res = requests.post("http://www.dogebug.online:9000/fuelcal/carSeries/", data=json.dumps(body), headers=headers)
            print(res)
        except:
            traceback.print_exc()
            sleep(1)
            pass
    f.close()
    print(len(l))


def import_model():
    f = open("CarInfo.txt")
    lines = f.readlines()

    l = []
    for line in lines:
        try:
            car_series = line.replace('\n', '').split(" ")[1].decode('utf-8')
            car_models = line.replace('\n', '').split(" ")[2:]
            car_model = ""
            for i in car_models:
                car_model += i+" "
            print(car_model)
            l.append(car_model)
            body = {
                "car_series": car_series,
                "car_model": car_model
            }
            res = requests.post("http://www.dogebug.online:9000/fuelcal/carModel/", data=json.dumps(body), headers=headers)
            print(res)
        except:
            traceback.print_exc()
            sleep(1)
            pass
    f.close()
    print(len(l))


if __name__ == '__main__':
    time1 = datetime.now()
    print(time1)
    import_brand()
    sleep(1)
    import_series()
    sleep(1)
    import_model()
    time2 = datetime.now()
    print(time2)
    print(str(time2-time1))
