#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/22 10:13
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_login.py
# @Software : PyCharm
import unittest
from ddt import ddt, data
from common.contants import FilePath
from common.request import HttpRequests
from common.mylog import Mylog
from common.do_testcase_excel import DoExcel

logger = Mylog("test login")


@ddt
class TestLogin(unittest.TestCase):

    filepath = FilePath()
    login_data = DoExcel(filepath.test_data_data(), "login").read_data()

    # @unittest.skip("login")
    @data(*login_data)
    def test_login(self, value):
        caseid = value["caseId"]
        title = value["title"]
        method = value["method"]
        url = self.filepath.api_url() + value["url"]
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
            DoExcel(FilePath().test_data_data(), "login").write_data(caseid + 1, 7, actual)
            DoExcel(FilePath().test_data_data(), "login").write_data(caseid + 1, 8, res)


if __name__ == '__main__':
    unittest.main()