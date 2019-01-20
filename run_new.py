#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/5 21:54
# @Author   :Yosef
# E-mail    :wurz529@foxmail.com
# File      :run_new.py
# Software  :PyCharm Community Edition
import unittest
import HTMLTestRunnerNew
# from test_case.test_math_method_new import TestMathMethod
from testcases.test_user import TestUser
from common.contants import FilePath
from common.send_mail import SendMail


suite = unittest.TestSuite()
loader = unittest.TestLoader()

suite.addTest(loader.loadTestsFromTestCase(TestUser))

# report_path = "result/reports/a.html"
report_path = FilePath().report_path()
print(report_path)

with open(report_path,"wb+") as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2,title="测试报告",description="这是描述细节",
                                              tester="夜雨声烦")
    runner.run(suite)

# mail = SendMail()
# mail.send_mail()