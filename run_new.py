#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/5 21:54
# @Author   :Yosef
# E-mail    :wurz529@foxmail.com
# File      :run_new.py
# Software  :PyCharm Community Edition
import unittest
import HTMLTestRunnerNew
from testcases.test_recharge import TestRecharge
from testcases.test_register import TestRegister
from testcases.test_login import TestLogin
from common.contants import FilePath
from common.send_mail import SendMail


suite = unittest.TestSuite()
loader = unittest.TestLoader()

suite.addTest(loader.loadTestsFromTestCase(TestRegister))
suite.addTest(loader.loadTestsFromTestCase(TestLogin))
suite.addTest(loader.loadTestsFromTestCase(TestRecharge))

# report_path = "result/reports/a.html"
report_path = FilePath().report_path()
print(report_path)

with open(report_path,"wb+") as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2,title="前程贷接口测试报告", description="",
                                              tester="夜雨声烦")
    runner.run(suite)

# mail = SendMail()
# mail.send_mail()