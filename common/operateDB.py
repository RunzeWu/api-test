#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/20 13:08
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :operateDB.py
# Software  :PyCharm Community Edition
import pymysql

class OperateDB:

    def __init__(self):
        self.database = pymysql.connect(
            host='test.lemonban.com',  # 如果是服务器，则输公网ip
            user='test',  # 当时设置的数据超级管理员账户
            passwd='test',  # 当时设置的管理员密码
            port=3306,  # MySQL数据的端口为3306，注意:切记这里不要写引号''
            database='future'  # 当时在MySQL中创建的数据库名字
        )
        self.cursor = self.database.cursor() # 获取一个游标 — 也就是开辟一个缓冲区，用于存放sql语句执行的结果

    def close_database(self):
        self.database.close()

    def query_the_largest_phone_number(self):
        # 执行sql语句,从sql中获取/选择数据,执行数据
        sql = "SELECT MAX(MobilePhone) FROM member;"
        self.cursor.execute(sql)

        data = self.cursor.fetchall()  # 获取所有的数据
        res = data[0][0]
        self.close_database()
        return res

    def query_leaveAmount(self, mobile):
        sql = "SELECT LeaveAmount FROM member WHERE MobilePhone=" + mobile + ";"
        print(sql)
        self.cursor.execute(sql)

        data = self.cursor.fetchall()  # 获取所有的数据
        res = data[0][0]
        self.close_database()
        return res



if __name__ == '__main__':
    A = OperateDB()
    res = A.query_leaveAmount("13755120067")
    print(res)