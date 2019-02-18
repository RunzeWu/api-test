#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/22 13:50
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_withdraw.py
# @Software : PyCharm
import unittest
import re
from libext.ddt import ddt, data
from common.contants import FilePath
from common.do_testcase_excel import DoExcel
from common.mysql import MysqlUtil
from common.mylog import Mylog
from common.request import HttpRequests

logger = Mylog("test_withdraw")


@ddt
class TestWithdraw(unittest.TestCase):
    filepath = FilePath()
    withdraw_data = DoExcel(filepath.test_data_data(), "withdraw").read_data()

    @classmethod
    def setUpClass(cls):
        logger.info("************开始执行withdraw模块测试用例*****************")
        cls.mysql = MysqlUtil()

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_database()
        logger.info("************withdraw模块测试用例脚本执行完毕*****************")

    def setUp(self):
        logger.info("*******开始执行测试用例*********")

    def tearDown(self):
        logger.info("*******本条测试用例执行完毕*********")

    @data(*withdraw_data)
    def test_withdrwa(self, value):
        caseid = value["caseId"]
        title = value["title"]
        method = value["method"]
        pre_url = value["pre_url"]
        pre_param = eval(value["pre_param"])
        url = value["url"]
        param = eval(value["param"])
        expected = eval(value["expected"])

        logger.info("开始执行caseId为[{}]的用例,用例标题是[{}],请求方式是[{}]".format(caseid, title, method))
        if pre_param is None:
            cookie = None
        else:
            cookie = HttpRequests(url=pre_url, params=pre_param).http_requests(method).cookies

        if param["mobilephone"] is None:
            param["mobilephone"] = ""
        # print(re.match(r"^1[35678]\d{9}$", param["mobilephone"]))
        if param is not None and re.match(r"^1[35678]\d{9}$", param["mobilephone"]) and param["mobilephone"] is not None:
            try:
                before_withdraw_amount = self.mysql.fetchone(
                    "select leaveamount from member where mobilephone=" + param["mobilephone"])
                before_withdraw_amount = float(before_withdraw_amount)
            except TypeError:
                logger.error("数据库中该{}号码不存在！".format(param["mobilephone"]))
                before_withdraw_amount = 0
            # print(before_recharge_amount, type(before_recharge_amount))
        else:
            before_withdraw_amount = 0
            logger.error("参数号码格式不正确")

        actual = HttpRequests(url, param).http_requests(method, cookies=cookie).json()
        print(actual["status"], type(actual["status"]))

        if actual["code"] == "10001":
            amount = float(param["amount"])

            after_withdraw_amount = before_withdraw_amount - amount

            res = "Failed"

            try:
                self.assertEqual(expected["code"], actual["code"])
                self.assertEqual(expected["msg"], actual["msg"])
                print(after_withdraw_amount, actual["data"]["leaveamount"])
                self.assertEqual(after_withdraw_amount, float(actual["data"]["leaveamount"]))
                self.assertEqual(expected["data"]["mobilephone"], actual["data"]["mobilephone"])
                self.assertEqual(expected["status"], actual["status"])
                res = "Pass"
            except AssertionError as e:
                logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
                raise e
            finally:
                DoExcel(FilePath().test_data_data(), "withdraw").write_data(caseid + 1, 9, str(actual))
                DoExcel(FilePath().test_data_data(), "withdraw").write_data(caseid + 1, 10, res)
        else:
            res = "Failed"
            try:
                self.assertEqual(expected, actual)
                res = "Pass"
            except AssertionError as e:
                logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
                raise e
            finally:
                DoExcel(FilePath().test_data_data(), "withdraw").write_data(caseid + 1, 9, str(actual))
                DoExcel(FilePath().test_data_data(), "withdraw").write_data(caseid + 1, 10, res)


if __name__ == '__main__':
    unittest.main()
