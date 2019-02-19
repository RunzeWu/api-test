#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/22 10:13
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_login.py
# @Software : PyCharm
import unittest
from libext.ddt import ddt, data
from common import contants
from common.request import HttpRequests
from common import mylog
from common.do_testcase_excel import DoExcel

logger = mylog.get_logger("case_login")


@ddt
class TestLogin(unittest.TestCase):

    # filepath = FilePath()
    login_data = DoExcel(contants.case_file, "login").read_data()

    @classmethod
    def setUpClass(cls):
        logger.info("************开始执行login模块测试用例*****************")

    @classmethod
    def tearDownClass(cls):
        logger.info("************login模块测试用例脚本执行完毕*****************")

    @data(*login_data)
    def test_login(self, value):
        caseid = value["caseId"]
        title = value["title"]
        method = value["method"]
        url = value["url"]
        param = eval(value["param"])
        expected = value["expected"]

        logger.info("当前模块是{},开始执行caseId为[{}]的用例,用例标题是[{}],请求方式是[{}]".format("login", caseid, title, method))

        myrequest = HttpRequests(url, param).http_requests(method)

        actual = myrequest.text
        try:
            self.assertEqual(expected, actual)
            res = "Pass"
        except Exception as e:
            logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
            res = "Failed"
            raise e
        finally:
            DoExcel(contants.case_file, "login").write_data(caseid + 1, 7, actual)
            DoExcel(contants.case_file, "login").write_data(caseid + 1, 8, res)


if __name__ == '__main__':
    unittest.main()