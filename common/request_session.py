#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/20 19:23
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :request_session.py
# Software  :PyCharm Community Edition
import requests
from common import mylog
from common.myjson import MyJson
from common.config import ReadConfig

mylog = mylog.get_logger("session_requset")


class Request:

    def __init__(self):
        self.session = requests.sessions.session()

    def request(self, url, method, params=None):
        method = method.upper()
        config = ReadConfig()
        pre_url = config.get_value("env-api", "pre_url")
        url = pre_url + url

        if params is not None and type(params) == str:
            params = MyJson().to_python_dict(params)

        if method == "GET":
            res = self.session.get(url=url, params=params)
            mylog.info('response: {0}'.format(res.text))
        elif method == "POST":
            res = self.session.post(url=url, data=params)
            mylog.info('response: {0}'.format(res.text))
        else:
            mylog.error("请检查请求方式是否正确")
            raise Exception("请检查请求方式是否正确")
        return res

    def close(self):
        self.session.close()  # 关闭session
