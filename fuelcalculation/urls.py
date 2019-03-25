# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2019/02/14 10:28"

from django.conf.urls import url
from .userviews import LoginViewSet, RegisterViewSet, ForgetPasswordViewSet, LogoutViewSet, UserInfoViewSet
from .userviews import CheckUserView
from .views import SendCodeView, SetCarInfoView, RefuelInfoView, FuelCalculationView, RankingListView
from .views import ExpenditureInfoView, CarCareInfoView


urlpatterns = [
    url(r'^login/$', LoginViewSet.as_view()),
    url(r'^register/$', RegisterViewSet.as_view()),
    url(r'^logout/$', LogoutViewSet.as_view()),
    url(r'^forgetPassword/$', ForgetPasswordViewSet.as_view()),
    url(r'^userInfo/$', UserInfoViewSet.as_view()),
    url(r'^checkUser/$', CheckUserView.as_view()),
    url(r'^sendCode/$', SendCodeView.as_view()),
    url(r'^setCarInfo/$', SetCarInfoView.as_view()),
    url(r'^reFuelInfo/$', RefuelInfoView.as_view()),
    url(r'^getFuelCal/$', FuelCalculationView.as_view()),
    url(r'^getRankList/$', RankingListView.as_view()),
    url(r'^expense/$', ExpenditureInfoView.as_view()),
    url(r'^carCare/$', CarCareInfoView.as_view()),

]
