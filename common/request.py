# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/13 17:10
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :request.py
# Software  :PyCharm Community Edition
import requests
from common.mylog import Mylog
from common.myjson import MyJson
from common.config import ReadConfig

logger = Mylog("http_requests")
pre_url = ReadConfig().get_value("env-api", "pre_url")
# print(pre_url)


class HttpRequests:
    def __init__(self, url, params=None, headers=None, json=None):
        self.url = pre_url + url
        self.params = params
        self.headers = headers
        self.json = json

    def http_requests(self, method, cookies=None):

        if self.params is not None and type(self.params)==str:
            self.params = MyJson().to_python_dict(self.params)

        if method.upper() == "GET":
            try:
                res = requests.get(self.url, params=self.params, headers=self.headers, cookies=cookies)
                logger.info("url:{}的get请求执行成功".format(self.url))
            except Exception as e:
                logger.info("执行get请求报错，报错信息是{}".format(e))
                res = e
        elif method.upper() == "POST":
            try:
                res = requests.post(self.url, data=self.params, headers=self.headers, json=self.json, cookies=cookies)
                logger.info("url:{}的post请求执行成功".format(self.url))
            except Exception as e:
                logger.info("执行post请求报错，报错信息是{}".format(e))
                res = e
        else:
            logger.info("请求方式不正确，请检查请求方式是否是get或者post")
            res = "请检查请求方式！！"

        return res


if __name__ == "__main__":
    url = "/member/login"
    url1 = "/member/withdraw"
    params = {"mobilephone": "17751810779", "pwd": "123456"}
    params1 = {"mobilephone": "17751810779", "amount": "500000"}
    res = HttpRequests(url, params).http_requests("get")
    print(HttpRequests(url, params).url)
    cookie = res.cookies
    res=HttpRequests(url1, params1).http_requests("get", cookies=cookie)
    print(res.json())


