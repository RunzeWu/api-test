#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/16 14:44
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_recharge.py
# @Software : PyCharm Community Edition
import unittest
import re
from libext.ddt import ddt, data
from common.contants import FilePath
from common.request import HttpRequests
from common.mylog import Mylog
from common.do_testcase_excel import DoExcel
from common.myjson import MyJson
from common.mysql import MysqlUtil

logger = Mylog("test_recharge")


@ddt
class TestRecharge(unittest.TestCase):
    filepath = FilePath()
    recharge_data = DoExcel(filepath.test_data_data(), "recharge").read_data()

    @classmethod
    def setUpClass(cls):
        logger.info("************开始执行recharge模块测试用例*****************")
        cls.mysql = MysqlUtil()

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_database()
        logger.info("************recharge模块测试用例脚本执行完毕*****************")

    def setUp(self):
        logger.info("*******开始执行测试用例*********")

    def tearDown(self):
        logger.info("*******本条测试用例执行完毕*********")

    @data(*recharge_data)
    def test_recharge(self, value):
        caseid = value["caseId"]
        title = value["title"]
        method = value["method"]
        pre_url = value["pre_url"]
        pre_param = MyJson().to_python_dict(value["pre_param"])
        url = value["url"]
        param = MyJson().to_python_dict(value["param"])
        expected = value["expected"]

        logger.info("开始执行caseId为[{}]的用例,用例标题是[{}],请求方式是[{}]".format(caseid, title, method))

        if param is not None and re.match(r"^1[35678]\d{9}$", param["mobilephone"]):
            before_recharge_amount = self.mysql.fetchone("select leaveamount from member where mobilephone="+param["mobilephone"])
            before_recharge_amount = float(before_recharge_amount)
            # print(before_recharge_amount, type(before_recharge_amount))
        else:
            before_recharge_amount = 0
            logger.error("参数号码格式不正确")

        cookie = HttpRequests(pre_url, pre_param).http_requests(method).cookies
        myrequest = HttpRequests(url, param).http_requests(method, cookies=cookie)

        actual = myrequest.text  # json类型字符串
        actual = MyJson().to_python_dict(actual)
        expected = MyJson().to_python_dict(expected)

        if actual["status"]:
            amount = float(param["amount"])

            after_recharge_amount = before_recharge_amount + amount

            try:
                self.assertEqual(expected["code"], actual["code"])
                self.assertEqual(expected["msg"], actual["msg"])
                self.assertEqual(after_recharge_amount, float(actual["data"]["leaveamount"]))
                self.assertEqual(expected["data"]["mobilephone"], actual["data"]["mobilephone"])
                self.assertEqual(expected["status"], actual["status"])
                res = "Pass"
            except AssertionError as e:
                logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
                res = "Failed"
                raise e
            finally:
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 9, str(actual))
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 10, res)
        else:
            try:
                self.assertEqual(expected, actual)
                res = "Pass"
            except AssertionError as e:
                logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
                res = "Failed"
                raise e
            finally:
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 9, str(actual))
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 10, res)


if __name__ == '__main__':
    unittest.main()
