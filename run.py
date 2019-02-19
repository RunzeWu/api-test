#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/5 21:54
# @Author   :Yosef
# E-mail    :wurz529@foxmail.com
# File      :run.py
# Software  :PyCharm Community Edition

import unittest
from libext import HTMLTestRunnerNew
from common import contants
# from testcases.test_recharge import TestRecharge
# from testcases.test_register import TestRegister
# from testcases.test_login import TestLogin
# from testcases.test_withdraw import TestWithdraw
# from common.send_mail import SendMail


# suite = unittest.TestSuite()
# loader = unittest.TestLoader()
#
# suite.addTest(loader.loadTestsFromTestCase(TestRegister))
# suite.addTest(loader.loadTestsFromTestCase(TestLogin))
# suite.addTest(loader.loadTestsFromTestCase(TestRecharge))
# suite.addTest(loader.loadTestsFromTestCase(TestWithdraw))

# 自动查找testcases目录下，以test开头的.py文件里面的测试类
discover = unittest.defaultTestLoader.discover(contants.testcases_dir, pattern="test_*.py", top_level_dir=None)

with open(contants.reports_html, "wb+") as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title="前程贷接口测试报告",
                                              description="测试了注册，登录，充值，取现模块的接口",
                                              tester="夜雨声烦")
    runner.run(discover)

# 通过Jenkins可以直接发送邮件，此处暂时忽略~
# mail = SendMail()
# mail.send_mail()