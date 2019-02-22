# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from fuelcalculation.models import UserProfile


class AdminLoginTest(TestCase):
    def setUp(self):
        UserProfile.objects.create_user(username='222', password='11111')

    def test_login_url(self):
        c = Client()
        response = c.post('/fuelcal/login/', {"username": "222", "password": "11111"})
        self.assertEqual(response.status_code, 200)


# class Demo(TestCase):
#     def setUp(self):
#         print('setUp')
#
#     def tearDown(self):
#         print('tearDown')
#
#     def test_demo(self):
#         print('test_demo')
#
#     def test_demo_2(self):
#         print('test_demo2')


