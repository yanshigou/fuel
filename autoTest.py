# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from usermanager.models import User


# class AdminLoginTest(TestCase):
#     def setUp(self):
#         User.objects.create_superuser(username='1', password='11111')
#
#     # url测试
#     def test_login_url(self):
#         c = Client()
#         response = c.post('/usermanager/login', {"username": "1", "password": "11111"})
#         self.assertEqual(response.status_code, 200)


class Demo(TestCase):
    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    def test_demo(self):
        print('test_demo')

    def test_demo_2(self):
        print('test_demo2')


