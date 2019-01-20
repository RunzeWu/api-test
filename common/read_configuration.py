# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/5 20:34
# @Author   :Yosef
# E-mail    :wurz529@foxmail.com
# File      :read_configuration.py
# Software  :PyCharm Community Edition
import configparser


class ReadConfig:
    def __init__(self, file):
        # mylog.info("开始读取配置文件")
        self.cf = configparser.ConfigParser()
        self.cf.read(file, encoding="utf-8")

    def get_value(self, section, option):
        return self.cf.get(section, option)

    def get_int(self, section, option):
        return self.cf.getint(section, option)

    def get_float(self, section, option):
        return self.cf.getfloat(section, option)

    def get_boolen(self, section, option):
        return self.cf.getfloat(section, option)


if __name__ == '__main__':
    res = ReadConfig("../conf/test.conf").get_value("test_case_id", "button")
    print(res)
