#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:anne.lin
@file:analyse.py.py
@time:2020/08/31
"""
from common import opmysql

operator_db = opmysql.OperationDbInterface(link_type=1) # 实例化自动化测试数据库操作类

class AnalyseData(object):
    """
    定义对接口测试数据进行分析的类，包含的方法有：
    1.导出测试数据到excel中
    """

    def __init__(self):

    def export2excel(self,names_export):
        """
        定义导出数据方法
        :param names_export:
        :return:
        """


if __name__ == '__main__':


