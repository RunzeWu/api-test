#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/8 16:01
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : contants.py
# @Software : PyCharm Community Edition
import os
import time
from common.read_configuration import ReadConfig


class FilePath:

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.dirname(__file__))

    def conf_path(self):
        path = os.path.join(self.dir_path, "conf", "test.conf")
        return path

    def test_data_data(self):
        path = os.path.join(self.dir_path, "datas", "user_test.xlsx")
        return path

    def receivers(self):
        path = os.path.join(self.dir_path, "datas", "receivers.xlsx")
        return path

    def report_path(self):
        report_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        report_name = report_time + " api test_report.html"
        path = os.path.join(self.dir_path, "reports", report_name)
        # path = ReadConfig(self.conf_path()).get_value("report","file_path")+report_name
        return path

    def log_path(self):
        log_time = time.strftime('%Y-%m-%d')
        path = os.path.join(self.dir_path, "logs", log_time + ".log")
        return path

    def api_url(self):
        button = ReadConfig(self.conf_path()).get_int("env-api", "button")

        """
        0 测试环境
        1 正式环境
        """
        if button == 0:
            api_url = "http://47.107.168.87:8080/futureloan/mvc/api"
        else:
            api_url = ""

        return api_url


if __name__ == '__main__':
    A = FilePath()
    print(A.api_url())