#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2018/12/13 15:26
# @Author   : Yosef-夜雨声烦
# @Email    : wurz529@foxmail.com
# @File     : send_mail.py
# @Software : PyCharm Community Edition
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from common import mylog
from common import contants
from common.do_receivers_excel import DoExcel as readreceiver

logger = mylog.get_logger("Sendmail")


class SendMail():
    def __init__(self):
        self.receivers = readreceiver(contants.receiver_file, "receivers").read_data()
        self.log_path = contants.logs_log
        self.report_path = contants.reports_html

    def send_mail(self):
        sender = "1054257352@qq.com"  # 发送者邮箱
        password = "thyscavhornxbfhc"  # 发送者密钥非密码

        receivers = self.receivers

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header("自动化测试程序", 'utf-8')
        message['To'] = Header("测试Manager", 'utf-8')
        subject = '本次自动化脚本执行完毕，详情请下载附件'
        message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText('本次自动化脚本执行完毕，结果见附件', 'plain', 'utf-8'))

        # 构造附件1，
        att1 = MIMEText(open(self.log_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename={}'.format(self.log_path)
        message.attach(att1)

        # 构造附件2，
        att2 = MIMEText(open(self.report_path, 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename={}'.format(self.report_path)
        message.attach(att2)

        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(sender, receivers, message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            logger.info("邮件发送成功")
        except Exception:
            logger.info("邮件发送失败")


if __name__ == "__main__":
    sendmail = SendMail()
    sendmail.send_mail()
