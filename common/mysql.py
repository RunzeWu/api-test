#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/20 13:08
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :mysql.py
# Software  :PyCharm Community Edition
import pymysql

class MysqlUtil:

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
        self.cursor.close()
        self.database.close()

    def fetchone(self, sql):
        # 执行SQL
        self.cursor.execute(sql)
        # 获取结果
        result = self.cursor.fetchone()
        return result[0]  # 返回结果


if __name__ == '__main__':
    A = MysqlUtil()
    sql = "select max(MobilePhone) from member"
    res = A.fetchone(sql)
    print(type(res))
    print(res)