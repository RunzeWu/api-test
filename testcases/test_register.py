#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/22 10:13
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_register.py
# @Software : PyCharm
import unittest
from ddt import ddt, data
from common.contants import FilePath
from common.request import HttpRequests
from common.mylog import Mylog
from common.do_testcase_excel import DoExcel
from common.mysql import MysqlUtil
from common.myjson import MyJson


filepath = FilePath()
reg_data = DoExcel(filepath.test_data_data(), "register").read_data()
logger = Mylog("test_register")

@ddt
class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("************开始执行register模块测试用例*****************")
        cls.mysql = MysqlUtil()


    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_database()

    def setUp(self):
        sql = "select max(mobilephone) from member"
        self.max_phone = self.mysql.fetchone(sql)

    # @unittest.skip("register")
    @data(*reg_data)
    def test_register(self, value):
        caseid = value["caseId"]
        title = value["title"]
        method = value["method"]
        url = filepath.api_url() + value["url"]
        param = MyJson().to_python_dict(value["param"])
        expected = value["expected"]
        logger.info("当前模块是{},开始执行caseId为[{}]的用例,用例标题是[{}],请求方式是[{}]".format("register", caseid, title, method))

        if param["mobilephone"] == "${mobile}":
            param["mobilephone"] = str(int(self.max_phone) + 1)

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
            DoExcel(FilePath().test_data_data(), "register").write_data(caseid + 1, 7, actual)
            DoExcel(FilePath().test_data_data(), "register").write_data(caseid + 1, 8, res)


if __name__ == '__main__':
    unittest.main()
