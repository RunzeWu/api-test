#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/20 19:23
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :request_session.py
# Software  :PyCharm Community Edition
import requests
from common.mylog import Mylog
from common.myjson import MyJson

mylog = Mylog("session_requset")


class Request:

    def __init__(self):
        self.session = requests.sessions.session()

    def request(self, url, method,params=None,data=None):
        method = method.upper()

        if params is not None and type(params) == str:
            params = MyJson().to_python_dict(params)

        if data is not None and type(data) == str:
            data = MyJson().to_python_dict(data)

        if method == "GET":
            res = self.session.get(url, params=params)
        elif method == "POST":
            res = self.session.post(url, data=data)
        else:
            mylog.error("请检查请求方式是否正确")
            raise Exception("请检查请求方式是否正确")
        return res
