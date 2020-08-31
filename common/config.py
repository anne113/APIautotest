#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:anne.lin
@file:config.py.py
@time:2020/08/31
"""
import os

src_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) #当前代码所在目录的上级目录

field_excel = {'编号', '接口名称', '用例级别', '请求类型', '接口地址', '接口头文件', '接口请求参数', '接口返回包', '待比较参数', '实际参数值', '参数完整性结果', '用例状态',
               '创建时间', '更新时间'}  # 导出的excel表格标题
