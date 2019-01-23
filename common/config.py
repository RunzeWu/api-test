# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/5 20:34
# @Author   :Yosef
# E-mail    :wurz529@foxmail.com
# File      :config.py
# Software  :PyCharm Community Edition
import configparser
from common.contants import FilePath

# config = configparser.ConfigParser()
# config.read(FilePath().global_conf_path())
# open = config.getboolean("switch", "open")
#
# if open:
#     config.read(FilePath().test_conf_path())
# else:
#     config.read(FilePath().prod_conf_path())
#
# value = config.get("env-api", "pre_url")
# print(value)


class ReadConfig:
    def __init__(self):

        self.cf = configparser.ConfigParser()
        self.cf.read(FilePath().global_conf_path(), encoding="utf-8")
        open = self.cf.getboolean("switch", "open")

        if open:
            self.cf.read(FilePath().test_conf_path(), encoding="utf-8")
        else:
            self.cf.read(FilePath().prod_conf_path(), encoding="utf-8")

    def get_value(self, section, option):
        return self.cf.get(section, option)

    def get_int(self, section, option):
        return self.cf.getint(section, option)

    def get_float(self, section, option):
        return self.cf.getfloat(section, option)

    def get_boolen(self, section, option):
        return self.cf.getfloat(section, option)


if __name__ == '__main__':
    res = ReadConfig().get_value("test_case_id", "button")
    print(res)
