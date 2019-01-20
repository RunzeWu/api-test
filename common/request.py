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

logger = Mylog("http_requests")


class HttpRequests:
    def __init__(self, url, params=None, data=None, headers=None, json=None):
        self.url = url
        self.params = params
        self.data = data
        self.headers = headers
        self.json = json

    def http_requests(self, method, cookies=None):

        if self.params is not None and type(self.params)==str:
            self.params = MyJson().to_python_str(self.params)

        if self.data is not None and type(self.data)==str:
            self.data = MyJson().to_python_str(self.data)

        if method.upper() == "GET":
            try:
                res = requests.get(self.url, self.params, headers=self.headers, cookies=cookies)
                logger.info("url:{}的get请求执行成功".format(self.url))
            except Exception as e:
                logger.info("执行get请求报错，报错信息是{}".format(e))
                res = e
        elif method.upper() == "POST":
            try:
                res = requests.post(self.url, data=self.data, headers=self.headers, json=self.json, cookies=cookies)
                logger.info("url:{}的post请求执行成功".format(self.url))
            except Exception as e:
                logger.info("执行post请求报错，报错信息是{}".format(e))
                res = e
        else:
            logger.info("请求方式不正确，请检查请求方式是否是get或者post")
            res = "请检查请求方式！！"

        return res


if __name__ == "__main__":
    url = "http://47.107.168.87:8080/futureloan/mvc/api/member/register"
    params = '{"mobilephone": "17751810779", "pwd": "123464", "regname": null}'
    data = {"mobilephone": "17751810779", "pwd": "123464", "regname": "夜雨声烦"}
    res = HttpRequests(url, params=params).http_requests("get")

    print(res.json())


