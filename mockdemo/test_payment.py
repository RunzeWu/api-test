#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/2/19 10:23
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_payment.py
# @Software : PyCharm
import unittest
from unittest import mock
import ddt

from mockdemo import payment


class PaymentTest(unittest.TestCase):

    def setUp(self):
        self.payment = payment.Payment()

    def test_success(self):
        self.payment.requestOutofSystem = mock.Mock(return_value=200)
        resp = self.payment.doPay(user_id=1, card_num='123445', amount=100)
        self.assertEqual('success', resp)

    def test_fail(self):
        self.payment.requestOutofSystem = mock.Mock(return_value=500)
        resp = self.payment.doPay(user_id=2, card_num='1234457', amount=10.01)
        self.assertEqual('fail', resp)

    def test_retry_success(self):
        # side_effect 必须是元祖、列表。str,字典等iterate数据类型
        self.payment.requestOutofSystem = mock.Mock(side_effect=[TimeoutError, 200])
        resp = self.payment.doPay(user_id=2, card_num='1234457', amount=10.01)
        print(resp)
        self.assertEqual('success', resp)
        # 判断mock方法被如何调用
        self.payment.requestOutofSystem.assert_called_with(user_id=3, card_num='1234457', amount=10.01)

    def test_retry_fail(self):
        self.payment.requestOutofSystem = mock.Mock(side_effect=[TimeoutError, 500])
        resp = self.payment.doPay(user_id=2, card_num='1234457', amount=10.01)
        print(resp)
        self.assertEqual('fail', resp)
        print('requestOutofSystem被调用两次：', self.payment.requestOutofSystem.call_count)