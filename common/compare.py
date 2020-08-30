#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:anne.lin
@file:compare.py.py
@time:2020/08/30
"""
import sys

from pip.utils import logging

from common import opmysql
from public import config

operation_db = opmysql.OperationDbInterface
class CompareParam(object):
    def __init__(self, param_interface):
        self.params_interface = param_interface  # 接口入参
        self.id_case = param_interface['id']  # 测试用id
        self.result_list_response = []  # 定义用来存储参数集的列表
        self.params_to_compare = param_interface['params_to_compare']  # 定义参数完整性预期结果


    def compare_code(self, result_interface):
        """
         定义关键参数值（code）比较
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = eval(result_interface)  # 将字符串转换成字典
                print("转换后的result_interface 是： ", temp_result_interface)
                temp_code_to_compare = self.params_interface['code_to_compare']  # 获取待比较code名称
                if temp_code_to_compare in temp_result_interface.keys():
                    if temp_result_interface[temp_code_to_compare] == self.params_interface['code_expect']:
                        result = {'code': '0000', 'message': '关键字参数值相同', 'data': []}
                        operation_db.op_sql(
                            "update case_interface set code_actual ='%s',result_code_compare = %s where id=%s" % (
                                temp_result_interface[temp_code_to_compare], 1, self.id_case))
                    elif unicode(str(temp_result_interface[temp_code_to_compare]),'utf-8') != unicode(str(self.params_interface['code_expect']),'utf-8'):
                        result = {'code':'1003','message':'关键字参数值不相同','data':[]}
                        operation_db.op_sql(
                            "update case_interface set code_actual ='%s',result_code_compare = %s  where id=%s" % (
                                temp_result_interface[temp_code_to_compare], 0, self.id_case))
                    else:
                        result = {'code': '1002', 'message': '关键字参数值比较错误', 'data': []}
                        operation_db.op_sql(
                            "update case_interface set code_actual ='%s',result_code_compare = %s where id=%s" % (
                                temp_result_interface[temp_code_to_compare], 3, self.id_case))
                else:
                    result = {'code': '1001', 'message': '返回包数据无关键字参数', 'data': []}
                    operation_db.op_sql("update case_interface set result_code_compare = %s  where id=%s" % (
                        2, self.id_case))
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
                operation_db.op_sql("update case_interface set result_code_compare = '%s'  where id=%s" % (
                    4, self.id_case))
        except Exception as e:
            result = {'code': '9999', 'message': '关键字参数值比较异常', 'data': []}
            operation_db.op_sql("update case_interface set result_code_compare = '%s'  where id=%s" % (
                                9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def get_compare_params(self,return_interface):
        """
        将接口返回数据中的参数写入列表中
        :param return_interface:
        :return:
        """
        try:
            if return_interface.startwith('{') and isinstance(return_interface, str):
                temp_result_interface = eval(return_interface)
                self.result_list_response = temp_result_interface.keys()
                result = {'code': '0000', 'message': '成功', 'data': self.result_list_response}
            else:
                result = {'code': '0000', 'message': '返回包格式不正确', 'data': []}
        except Exception as e: #记录日志到log.txt文件
            result = {'code': '9999', 'message': '处理数据异常', 'data': []}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def compare_params_complete(self,result_interface):
        """
        参数完整性比较方法，传参值与__recur_params方法返回结果比较
        :param result_interface:接口http返回包
        :return:返回码code，返回信息message，数据data
        """
        temp_compare_params = self.__recur_params(result_interface) # 获取返回包参数集
        if temp_compare_params['code'] == '0000':
            temp_result_list_response = temp_compare_params['data'] # 获取接口返回参数去重列表
            if self.params_to_compare == '' or isinstance(self.params_to_compare,(tuple,dict)): # 判断用例数据为空或类型不符合
                result = {'code':'4001','message':'用例中待比较参数集错误','data':self.params_to_compare}
            else:
                list_params_to_compare = eval(self.params_to_compare) # 将数据表中unicode编码转换成原列表
                if


    def __recur_params(self,result_interface):
        """
        定义递归操作，将接口返回数据中参数名写入列表中（去重）
        :param result_interface:
        :return:
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface,str):
                temp_result_interface = eval(result_interface)
                self.__recur_params(temp_result_interface)
            elif result_interface.startswith('{') and isinstance(result_interface,dict):
                for param,value  in result_interface.items():
                    self.result_list_response.append(param)
                    if isinstance(value,list):
                        for param in list:
                            self.__recur_params(param)
                    elif isinstance(value,dict):
                        self.__recur_params(value)
                    else:
                        continue
            else:
                pass
        except Exception as e:
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return {'code':'9999','message':'处理数据异常',data:[]}
        return {'code':'0000','message':'成功','data':list(set(self.result_list_response))}


if __name__ == '__main__':
