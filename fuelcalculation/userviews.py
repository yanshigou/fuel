# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2019/02/14 14:59"

from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .functions import is_user_exist, http_response
from .models import UserProfile
import traceback


# 用户管理模块
class LoginViewSet(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                nickname = user.nickname
                data = {"username": username, "nickname": nickname}
                return http_response(data=data)
            return http_response(error_no=6, info="username or password Error")
        except KeyError:
            traceback.print_exc()
            return http_response(error_no=1, info="input error")
        except UserProfile.DoesNotExist:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


class RegisterViewSet(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            if is_user_exist(username):
                return http_response(error_no=43, info="user existed")
            password = request.data.get('password')
            nickname = request.data.get('nickname')
            sex = request.data.get('sex')
            image = request.FILES.get('image')
            if image is None:
                image = ""
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.nickname = nickname
            user_profile.sex = sex
            user_profile.image = image
            user_profile.password = make_password(password)
            user_profile.save()
            resdata = {"username": username, "nickname": nickname}
            return http_response(data=resdata)
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


class ForgetPasswordViewSet(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            newpassword = request.data.get('newpassword')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            if newpassword is None:
                return http_response(error_no=5, info='newpassword is none')
            user = UserProfile.objects.get(username=username)
            user.set_password(newpassword)
            user.save()
            return http_response(info="Success")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def put(self, request):
        try:
            username = request.data.get('username')
            oldpassword = request.data.get('oldpassword')
            newpassword = request.data.get('newpassword')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            user = UserProfile.objects.get(username=username)
            if user.check_password(oldpassword):
                user.set_password(newpassword)
                user.save()
                return http_response()
            return http_response(error_no=5, info='oldpassword error')
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


class LogoutViewSet(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            print(username)
            return http_response()
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


class UserInfoViewSet(APIView):
    def get(self, request):
        try:
            username = request.query_params['username']
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            user = UserProfile.objects.get(username=username)
            nickname = user.nickname
            sex = user.sex
            data = {"username": username, "nickname": nickname, "sex": sex}
            return http_response(data=data)
        except KeyError:
            traceback.print_exc()
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")

    def put(self, request):
        try:
            username = request.data.get('username')
            if not is_user_exist(username):
                return http_response(error_no=42, info="No User")
            user = UserProfile.objects.get(username=username)
            user.nickname = request.data.get("nickname")
            user.sex = request.data.get("sex")
            temphead = request.FILES.get("image")
            if temphead is not None:
                user.image = temphead
                user.save()
                return http_response(data={"head": user.objects.get(username=username).image.url})
            else:
                user.save()
                return http_response(info="Success")
        except KeyError:
            traceback.print_exc()
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


class CheckUserView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            if is_user_exist(username):
                return http_response(error_no=20, info="user existed")
            else:
                return http_response(error_no=19, info="user unexisted")
        except KeyError:
            return http_response(error_no=1, info="input error")
        except:
            traceback.print_exc()
            return http_response(error_no=2, info="cmx exception")


