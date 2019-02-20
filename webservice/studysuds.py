#！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/2/20 23:02
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :studysuds.py
# Software  :PyCharm Community Edition
from suds.client import Client

user_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
client=Client(user_url)#Client里面直接放访问的URL，可以生成一个webservice对象

print(client)#打印所webservice里面的所有接口方法名称，结果如下截图所示：
t={"channel_id":2,"ip":"129.45.6.7","mobile":17751810000 ,"pwd":"123456","user_id" :"shabicu8","verify_code":'123456'}#用字典的方式传值

result=client.service.userRegister(t)
#client这个对象 ，调用service这个方法，然后再调用userRegister这个接口函数，函数里面传递刚刚我们准备
#好的得参数字典 t
print(result)#打印返回结果