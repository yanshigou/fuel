# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2019/02/14 10:28"

from django.conf.urls import url
from .userviews import LoginViewSet, RegisterViewSet, ForgetPasswordViewSet, LogoutViewSet, UserInfoViewSet
from .userviews import CheckUserView
from .views import SendCodeView, SetCarInfoView, RefuelInfoView



urlpatterns = [
    url(r'^login/$', LoginViewSet.as_view()),
    url(r'^register/$', RegisterViewSet.as_view()),
    url(r'^logout/$', LogoutViewSet.as_view()),
    url(r'^forgetpassword/$', ForgetPasswordViewSet.as_view()),
    url(r'^userinfo/$', UserInfoViewSet.as_view()),
    url(r'^checkuser/$', CheckUserView.as_view()),
    url(r'^sendcode/$', SendCodeView.as_view()),
    url(r'^setcarinfo/$', SetCarInfoView.as_view()),
    url(r'^refuelinfo/$', RefuelInfoView.as_view()),

]
