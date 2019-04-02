# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models


# 继承自带的User表 再添加需要的其他字段
class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    sex = models.CharField(max_length=10, verbose_name=u'性别')
    image = models.ImageField(upload_to="image/%Y/%m", default='', max_length=100)

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = "用户信息表"


# 车辆信息表
class CarInfo(models.Model):
    username = models.ForeignKey(UserProfile, to_field="username", verbose_name=u'用户')
    car_id = models.CharField(max_length=20, unique=True, verbose_name=u'车牌号')
    car_brand = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'汽车品牌')
    car_name = models.CharField(max_length=10, default=u'我的小车', verbose_name=u'汽车昵称')
    car_series = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'车系')
    car_model = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'车型')


# 燃料类型表
class FuelType(models.Model):
    fuel_type = models.CharField(max_length=10, default=u'未指定燃料类型', unique=True, verbose_name=u'燃料类型')


# 加油记录表
class RefuelInfo(models.Model):
    car_id = models.ForeignKey(CarInfo, to_field='car_id', verbose_name='车牌号')
    fuel_type = models.ForeignKey(FuelType, to_field="fuel_type", verbose_name=u'燃料类型')
    time = models.DateTimeField(verbose_name=u'加油时间')
    is_full = models.IntegerField(default=1, verbose_name=u'是否加满')
    is_light = models.IntegerField(default=0, verbose_name=u'是否亮油灯')
    is_norecord = models.IntegerField(default=0, verbose_name=u'上一次没有记录')
    mileages = models.CharField(max_length=10, verbose_name=u'里程碑总数/公里')
    prices = models.CharField(max_length=10, verbose_name=u'单价/元')
    moneys = models.CharField(max_length=10, verbose_name=u'总金额/元')
    fuel_counts = models.CharField(max_length=10, verbose_name=u'油量/升')
    fuel_station = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'加油站')
    remark = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'备注')


# 油耗记录表
class FuelInfo(models.Model):
    id = models.OneToOneField(RefuelInfo, to_field='id', primary_key=True)
    car_id = models.ForeignKey(CarInfo, to_field='car_id', verbose_name='车牌号')
    time = models.DateTimeField(verbose_name=u'加油时间')
    fuel_l_km = models.CharField(max_length=10, default='?', verbose_name=u'油耗升/百公里')
    fuel_y_km = models.CharField(max_length=10, default='?', verbose_name=u'油耗元/百公里')
    mileages = models.CharField(max_length=10, verbose_name=u'里程碑总数/公里')
    driving_km = models.CharField(max_length=10, verbose_name=u'本次行驶里程/公里')
    driving_moneys = models.CharField(max_length=10, verbose_name=u'本次行驶金额/元')
    driving_fuel_counts = models.CharField(max_length=10, verbose_name=u'本次行驶使用油量/升')


# 支出费用详情表
class ExpenditureInfo(models.Model):
    car_id = models.ForeignKey(CarInfo, to_field='car_id', verbose_name='车牌号')
    time = models.DateTimeField(verbose_name=u'时间')
    remark = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'备注')
    moneys = models.CharField(max_length=10, verbose_name=u'金额/元')
    info = models.CharField(max_length=10, verbose_name=u'用途')


# 排行列表
class RankingList(models.Model):
    username = models.ForeignKey(UserProfile, to_field="username", verbose_name=u'用户')
    car_id = models.ForeignKey(CarInfo, to_field='car_id', verbose_name='车牌号')
    average_fuel_l_km = models.CharField(max_length=10, default='?', verbose_name=u'平均油耗升/百公里')
    average_fuel_y_km = models.CharField(max_length=10, default='?', verbose_name=u'平均油耗元/百公里')
    km = models.CharField(max_length=10, verbose_name=u'总里程/公里')
    sum_km = models.CharField(max_length=10, verbose_name=u'总记录里程/公里')
    sum_moneys = models.CharField(max_length=10, verbose_name=u'总花费金额/元')
    sum_fuel_counts = models.CharField(max_length=10, verbose_name=u'总加了油量/升')


# 车辆保养信息记录
class CarCareInfo(models.Model):
    caretype = (
        (0, '常规保养'),
        (1, '定期保养'),
        (2, '大保养'),
    )
    car_id = models.ForeignKey(CarInfo, to_field='car_id', verbose_name='车牌号')
    time = models.DateTimeField(verbose_name=u'保养时间')
    km = models.CharField(max_length=10, verbose_name=u'保养时总里程/公里')
    care_type = models.IntegerField(default=0, verbose_name=u'保养类型', choices=caretype)
    next_time = models.DateTimeField(verbose_name=u'预计下一次保养时间')
    next_km = models.CharField(max_length=10, verbose_name=u'预计下一次保养总里程/公里')
    remark = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'备注')


# 订单信息表
class OrderInfo(models.Model):
    pay_type = (
        (1, '微信'),
        (2, '支付宝')
    )
    pay_status = (
        (0, '未支付'),
        (1, '已支付'),
        (-1, '已关闭')
    )
    ordernum = models.CharField(max_length=40, default="", verbose_name='商家订单号')
    ordertime = models.DateTimeField(verbose_name='创建时间')
    orderuser = models.ForeignKey(UserProfile, to_field="username", verbose_name='用户')
    ordermoney = models.FloatField(verbose_name='金额/分')
    order_paytype = models.IntegerField(default=1, choices=pay_type, verbose_name='支付方式')  # 1--微信 2--支付宝
    order_paynum = models.CharField(max_length=40, default="", verbose_name='平台订单号')
    orderstatus = models.IntegerField(default=0, choices=pay_status, verbose_name='订单状态')

    class Meta:
        verbose_name = "订单信息表"
        verbose_name_plural = "订单信息表"


# 车辆品牌表
class CarBrandInfo(models.Model):
    car_brand = models.CharField(max_length=10, unique=True, verbose_name=u'汽车品牌')


# 车辆车系表
class CarSeriesInfo(models.Model):
    car_brand = models.ForeignKey(CarBrandInfo, to_field='car_brand', verbose_name=u'汽车品牌')
    car_series = models.CharField(max_length=10, unique=True, verbose_name=u'车系')


# 车辆车型表
class CarModelInfo(models.Model):
    car_series = models.ForeignKey(CarSeriesInfo, to_field='car_series', verbose_name=u'车系')
    car_model = models.CharField(max_length=20, verbose_name=u'车型')