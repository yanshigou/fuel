# -*- coding: utf-8 -*-
__author__ = 'dzt'
__date__ = '2019/04/02 10:33'

from xadmin.plugins.auth import UserAdmin
import xadmin
from xadmin import views
from .models import UserProfile, CarInfo, FuelType, RefuelInfo, FuelInfo, ExpenditureInfo, RankingList, CarCareInfo
from .models import OrderInfo, CarBrandInfo, CarSeriesInfo, CarModelInfo


class UserProfileAdmin(UserAdmin):
    pass


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "狗子油耗后台管理系统"
    site_footer = "dogeFule"
    menu_style = 'accordion'


class CarInfoAdmin(object):
    list_display = ['username', 'car_id', 'car_brand', 'car_name', 'car_series', 'car_model']


class FuelTypeAdmin(object):
    list_display = ['fuel_type', ]


class RefuelInfoAdmin(object):
    list_display = ['car_id', 'fuel_type', 'time', 'is_full', 'is_light', 'is_norecord', 'mileages', 'prices', 'moneys',
                    'fuel_counts', 'fuel_station', 'remark']


class FuelInfoAdmin(object):
    list_display = ['car_id', 'time', 'fuel_l_km', 'fuel_y_km', 'mileages', 'driving_km', 'driving_moneys',
                    'driving_fuel_counts']


class ExpenditureInfoAdmin(object):
    list_display = ['car_id', 'time', 'remark', 'moneys', 'info']


class RankingListAdmin(object):
    list_display = ['username', 'car_id', 'average_fuel_l_km', 'average_fuel_y_km', 'km', 'sum_km', 'sum_moneys',
                    'sum_fuel_counts']


class CarCareInfoAdmin(object):
    list_display = ['car_id', 'time', 'km', 'care_type', 'next_time', 'next_km', 'remark']


class OrderInfoAdmin(object):
    list_display = ['ordernum', 'ordertime', 'orderuser', 'ordermoney', 'order_paytype', 'order_paynum', 'orderstatus']


class CarBrandInfoAdmin(object):
    list_display = ['car_brand']


class CarSeriesInfoAdmin(object):
    list_display = ['car_brand', 'car_series']


class CarModelInfoAdmin(object):
    list_display = ['car_series', 'car_model']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(CarInfo, CarInfoAdmin)
xadmin.site.register(FuelType, FuelTypeAdmin)
xadmin.site.register(RefuelInfo, RefuelInfoAdmin)
xadmin.site.register(FuelInfo, FuelInfoAdmin)
xadmin.site.register(ExpenditureInfo, ExpenditureInfoAdmin)
xadmin.site.register(RankingList, RankingListAdmin)
xadmin.site.register(CarCareInfo, CarCareInfoAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(CarBrandInfo, CarBrandInfoAdmin)
xadmin.site.register(CarSeriesInfo, CarSeriesInfoAdmin)
xadmin.site.register(CarModelInfo, CarModelInfoAdmin)
