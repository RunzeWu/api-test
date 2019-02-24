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
        cls.admin_request = Request() # 实例化对象
        cls.request = Request()
        cls.mysql = MysqlUtil()
        # 前提条件1： 管理员登录，加标，审核
        admin_login_param = '{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'
        admin_login_param = context.replace_new(admin_login_param)
        cls.admin_request.request("/member/login", "get", params=admin_login_param)
        logger.info("管理员登录完成")

        admin_add_param = '{"memberId":"${loan_member_id}","title":"add_loan_test by YYSF","amount":20000,"loanRate":"12.0","loanTerm":3,"loanDateType":0,"repaymemtWay":11,"biddingDays":5}'
        admin_add_param = context.replace_new(admin_add_param)
        cls.admin_request.request("/loan/add","get",params=admin_add_param)

        loan_member_id = getattr(Context, "loan_member_id")
        loan_id_sql="select id from loan where memberID='{0}'" \
            " order by createTime desc limit 1".format(loan_member_id)
        loan_id = cls.mysql.fetchone(loan_id_sql)[0]
        logger.info("管理员加标完成")
        setattr(Context, 'loan_id', str(loan_id))

        admin_audit_param = {"id":loan_id,"status":4}
        cls.admin_request.request("/loan/audit","post",params=admin_audit_param)
        logger.info("管理员审核完成")

        #前提条件2：用户正常登录
        login_param='{"mobilephone":"${normal_user}","pwd":"${normal_pwd}"}'
        login_param = context.replace_new(login_param)
        cls.request.request("/member/login","post",params=login_param)
        logger.info("投资人登录成功")


    @classmethod
    def tearDownClass(cls):
        cls.admin_request.close()  # 关闭session
        cls.request.close()
        cls.mysql.close_database()  # 关闭MySQL

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*cases)
    def test_invest(self, case):
        param = eval(context.replace_new(case["data"]))
        resp = self.request.request(case["url"], case["method"], params=param)
        # logger.info("请求结果是{}".format(resp.text))

        try:
            # 先判断状态码
            self.assertEqual(case["expect"], int(resp.json()["code"]), "invest error")
            logger.info("状态码一致")

            sql = "select * FROM invest WHERE LoanId = '{0}' ORDER BY CreateTime DESC LIMIT 1".format(getattr(Context,'loan_id'))
            res = self.mysql.fetchone(sql)
            db_MemberId = res[1]
            db_Amount = res[3]
            # 状态码11001查库是否成功，非查看是否不成功
            if resp.json()["code"] == "10001":
                self.assertEqual(db_MemberId, int(Context.normal_member_id))
                self.assertEqual(int(db_Amount), int(param["amount"]))
                logger.info("数据验证通过")
            else:
                # self.assertNotEqual(db_MemberId, int(Context.normal_member_id))
                if param["amount"] is None:
                    param["amount"] = 0
                self.assertNotEqual(int(db_Amount), int(param["amount"]))
                logger.info('数据验证通过')
            self.do_excel.write_data(case["case_id"] + 1, 7, resp.text)
            self.do_excel.write_data(case["case_id"] + 1, 8, "Pass")
        except AssertionError as e:
            self.do_excel.write_data(case["case_id"]+1, 8, "Failed")
            self.do_excel.write_data(case["case_id"] + 1, 7, resp.text)
            logger.error("第{0}用例执行结果：FAIL".format(case["case_id"]))
            raise e


if __name__ == '__main__':
    unittest.main()