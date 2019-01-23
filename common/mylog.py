# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/6 16:52
# @Author   :Yosef
# E-mail    :wurz529@foxmail.com
# File      :mylog.py
# Software  :PyCharm Community Edition
import logging
from common.config import ReadConfig
from common.contants import FilePath


class Mylog:
    def __init__(self, log_name):
        self.log_name = log_name
        self.in_level = ReadConfig().get_value("log", "in_level")
        self.ch_level = ReadConfig().get_value("log", "ch_level")
        self.fh_level = ReadConfig().get_value("log", "fh_level")
        self.formatter = ReadConfig().get_value("log", "formatter")

    def mylog(self, level, msg):
        logger = logging.Logger(self.log_name)
        logger.setLevel(self.in_level)
        formatter = logging.Formatter(self.formatter)

        ch = logging.StreamHandler()
        ch.setLevel(self.ch_level)
        ch.setFormatter(formatter)

        fh = logging.FileHandler(FilePath().log_path(), encoding="utf-8")
        fh.setLevel(self.fh_level)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        if level == "DEBUG":
            logger.debug(msg)
        elif level == "INFO":
            logger.info(msg)
        elif level == "WARNING":
            logger.warning(msg)
        elif level == "ERROR":
            logger.error(msg)
        else:
            logger.critical(msg)

        logger.removeHandler(fh)
        fh.close()
        logger.removeHandler(ch)

    def debug(self, msg):
        self.mylog("DEBUG", msg)

    def info(self, msg):
        self.mylog("INFO", msg)

    def warning(self, msg):
        self.mylog("WARNING", msg)

    def error(self, msg):
        self.mylog("ERROR", msg)

    def critical(self, msg):
        self.mylog("CRITICAL", msg)


if __name__ == '__main__':
    logger = Mylog("testlog")
    logger.info("****************")
    logger.debug("----------------")
    logger.warning("+++++++++++++++")
    logger.error("////////////////")
    logger.critical("/*-/*-/-*/*-*/")
