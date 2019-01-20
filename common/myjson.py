# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :2019/1/13 17:17
# @Author   :Yosef-夜雨声烦
# E-mail    :wurz529@foxmail.com
# File      :myjson.py
# Software  :PyCharm Community Edition
import json
import jsonpath

class MyJson:
    def to_json(self, obj):
        res = json.dumps(obj, indent=4, sort_keys=True, separators=(',', ': '))
        return res

    def to_python_str(self, obj):
        res = json.loads(obj, encoding="utf-8")
        return res

    def to_result(self, json_str, expr):
        json_obj = self.to_python_str(json_str)
        result = jsonpath.jsonpath(json_obj, expr)
        # 返回的是result，list
        return result


if __name__ == '__main__':
    A = MyJson()
    data = {'data': None, 'status': 0, 'msg': '手机号码格式不正确', 'code': '20109'}
    res = A.to_json(data)
    print(res)
    res = A.to_result(res,"$.status")
    print(res)
    for item in res:
        print(item)
    # res = A.to_python(res)
    # print(res)
