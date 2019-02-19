#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/2/19 10:23
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : study_mock.py
# @Software : PyCharm

import requests
from unittest import mock


def request_baidu():
    return requests.get('http://www.baidu.com').text.encode('utf-8')


def print_baidu():
    print(request_baidu())


request_baidu = mock.Mock(return_value="this is baidu")
print_baidu()