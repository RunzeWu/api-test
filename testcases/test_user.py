#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/1/16 14:44
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_user.py
# @Software : PyCharm Community Edition
import unittest
from ddt import ddt, data
from common.contants import FilePath
from common.request import HttpRequests
from common.mylog import Mylog
from common.do_testcase_excel import DoExcel
from common.myjson import MyJson
from common.operateDB import OperateDB

filepath = FilePath()
# reg_data = DoExcel(filepath.test_data_data(), "register").read_data()
# login_data = DoExcel(filepath.test_data_data(), "login").read_data()
recharge_data = DoExcel(filepath.test_data_data(), "recharge").read_data()
logger = Mylog("test_user")


@ddt
class TestUser(unittest.TestCase):
    """
    测试前程贷接口的用户模块
    """

    def setUp(self):
        logger.info("*******开始执行测试用例*********")

    def tearDown(self):
        logger.info("*******本条测试用例执行完毕*********")

    # @data(*reg_data)
    # def test_register(self, value):
    #     # print(value)
    #     caseid = value["caseId"]
    #     title = value["title"]
    #     method = value["method"]
    #     url = filepath.api_url() + value["url"]
    #     param = value["param"]
    #     expected = value["expected"]
    #     # print(caseid, title, method, url, param, expected, end="")
    #     logger.info("当前模块是{},开始执行caseId为[{}]的用例,用例标题是[{}],请求方式是[{}]".format("register", caseid, title, method))
    #     if method.upper() == "GET":
    #         myrequest = HttpRequests(url, params=param).http_requests(method)
    #     else:
    #         myrequest = HttpRequests(url, data=param).http_requests(method)
    #     actual = myrequest.text
    #     # print(actual)
    #     # print("[{}]".format(actual))
    #     try:
    #         self.assertEqual(expected, actual)
    #         res = "Pass"
    #     except Exception as e:
    #         logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
    #         res = "Failed"
    #         raise e
    #     finally:
    #         # actual = str(MyJson().to_python_str(actual))
    #         DoExcel(FilePath().test_data_data(), "register").write_data(caseid + 1, 7, actual)
    #         DoExcel(FilePath().test_data_data(), "register").write_data(caseid + 1, 8, res)
    #
    # @data(*login_data)
    # def test_login(self, value):
    #     # time.sleep(5)
    #     caseid = value["caseId"]
    #     title = value["title"]
    #     method = value["method"]
    #     url = filepath.api_url()+value["url"]
    #     param = eval(value["param"])
    #     expected = value["expected"]
    #     # print(caseid, title, method, url, param, expected, end="\n")
    #
    #     logger.info("当前模块是{},开始执行caseId为[{}]的用例,用例标题是[{}],请求方式是[{}]".format("login", caseid, title, method))
    #     # headers = {'Connection': 'close',}
    #
    #     if method.upper() == "GET":
    #         myrequest = HttpRequests(url, params=param).http_requests(method)
    #     else:
    #         myrequest = HttpRequests(url, data=param).http_requests(method)
    #
    #     actual = myrequest.text
    #     # print(actual)
    #     # print("[{}]".format(actual))
    #     try:
    #         self.assertEqual(expected, actual)
    #         res = "Pass"
    #     except Exception as e:
    #         logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
    #         res = "Failed"
    #         raise e
    #     finally:
    #         # actual = str(MyJson().to_python_str(actual))
    #         DoExcel(FilePath().test_data_data(), "login").write_data(caseid + 1, 7, actual)
    #         DoExcel(FilePath().test_data_data(), "login").write_data(caseid + 1, 8, res)


    @data(*recharge_data)
    def test_recharge(self, value):
        caseid = value["caseId"]
        title = value["title"]
        method = value["method"]
        pre_url = filepath.api_url() + value["pre_url"]
        pre_param = eval(value["pre_param"])
        url = filepath.api_url() + value["url"]
        param = eval(value["param"])
        expected = value["expected"]



        logger.info("开始执行caseId为[{}]的用例,用例标题是[{}],请求方式是[{}]".format(caseid, title, method))
        cookie = HttpRequests(pre_url, data=pre_param).http_requests("post").cookies

        mobile = param["mobilephone"]
        before_recharge_amount = float('%.2f' %(OperateDB().query_leaveAmount(mobile)))

        if method.upper() == "GET":
            myrequest = HttpRequests(url, params=param).http_requests(method, cookies=cookie)
        else:
            myrequest = HttpRequests(url, data=param).http_requests(method, cookies=cookie)

        actual = myrequest.text  # json类型字符串
        actual = MyJson().to_python_dict(actual)
        expected = MyJson().to_python_dict(expected)

        if actual["status"]:


            amount=float(param["amount"])

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
                # actual = str(MyJson().to_python_str(actual))
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 9, str(actual))
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 10, res)
        else:
            try:
                self.assertEqual(expected,actual)
            except AssertionError as e:
                logger.warning("实际结果与预期结果不同，实际结果:{},预期结果:{}".format(actual, expected))
                res = "Failed"
                raise e
            finally:
                # actual = str(MyJson().to_python_str(actual))
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 9, str(actual))
                DoExcel(FilePath().test_data_data(), "recharge").write_data(caseid + 1, 10, res)


if __name__ == '__main__':
    unittest.main()
