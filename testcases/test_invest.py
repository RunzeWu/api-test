#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/2/20 13:15
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : test_invest.py
# @Software : PyCharm

import unittest
from common import contants
from common import context
from common import mylog
from common.context import Context
from common.do_testcase_excel import DoExcel
from common.mysql import MysqlUtil
from common.request_session import Request
from libext.ddt import ddt, data

logger = mylog.get_logger("invest_test")

@ddt
class TestInvest(unittest.TestCase):
    do_excel = DoExcel(contants.case_file, "invest")
    cases = do_excel.read_data()

    @classmethod
    def setUpClass(cls):
        cls.request = Request()  # 实例化对象
        cls.mysql = MysqlUtil()

    @classmethod
    def tearDownClass(cls):
        cls.request.close()  # 关闭session
        cls.mysql.close_database()  # 关闭MySQL

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*cases)
    def test_invest(self, case):
        param = context.replace_new(case["data"])
        resp = self.request.request(case["url"], case["method"], params=param)

        try:
            self.assertEqual(case["expect"], int(resp.json()["code"]), "invest error")
            self.do_excel.write_data(case["case_id"]+1, 7, resp.text)
            self.do_excel.write_data(case["case_id"]+1, 8, "Pass")

            if resp.json()["msg"] == "加标成功":
                loan_member_id = getattr(Context, "loan_member_id")
                sql = "select id from future.loan where memberID='{0}'" \
                      " order by createTime desc limit 1".format(loan_member_id)

                loan_id = self.mysql.fetchone(sql)

                setattr(Context, 'loan_id', str(loan_id))
        except AssertionError as e:
            self.do_excel.write_data(case["case_id"]+1, 8, "Failed")
            logger.error("第{0}用例执行结果：FAIL".format(case["case_id"]))
            raise e


if __name__ == '__main__':
    unittest.main()