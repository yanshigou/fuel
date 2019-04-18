# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2019/4/18"


import requests
import json
from time import sleep
from datetime import datetime

headers = {'content-type': 'application/json'}


def import_brand():
    f = open("CarInfo.txt")
    lines = f.readlines()

    l = []
    for line in lines:
        car_brand = line.replace('\n', '').split(" ")[0].decode('utf-8')
        print(car_brand)
        if car_brand in l:
            continue
        l.append(car_brand)
        body = {
            "car_brand": car_brand
        }
        res = requests.post("http://127.0.0.1:8000/fuelcal/carBrand/", data=json.dumps(body), headers=headers)
        print(res)
    f.close()
    print(len(l))


def import_series():
    f = open("CarInfo.txt")
    lines = f.readlines()

    l = []
    for line in lines:
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
        res = requests.post("http://127.0.0.1:8000/fuelcal/carSeries/", data=json.dumps(body), headers=headers)
        print(res)
    f.close()
    print(len(l))


def import_model():
    f = open("CarInfo.txt")
    lines = f.readlines()

    l = []
    for line in lines:
        car_series = line.replace('\n', '').split(" ")[1].decode('utf-8')
        car_models = line.replace('\n', '').split(" ")[2:]
        car_model = ""
        for i in car_models:
            car_model += i+" "
        print(car_model)
        if car_model in l:
            continue
        l.append(car_model)
        body = {
            "car_series": car_series,
            "car_model": car_model
        }
        res = requests.post("http://127.0.0.1:8000/fuelcal/carModel/", data=json.dumps(body), headers=headers)
        print(res)
    f.close()
    print(len(l))


if __name__ == '__main__':
    time1 = datetime.now()
    import_brand()
    sleep(1)
    import_series()
    sleep(1)
    import_model()
    time2 = datetime.now()
    print(str(time2-time1))
