#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:anne.lin
@file:request.py
@time:2020/08/24
"""
import logging

import requests

from common import opmysql
from public import config


class RequestInterface(object):
    def __new_params(self, param):
        try:
            if isinstance(param, str) and param.startswith('{'):
                new_param = eval(param)
            elif param == None:
                new_param = ''
            else:
                new_param = param
        except Exception as e:
            new_param = ''
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return new_param

    def __http_post(self, interface_url, headerdata, interface_param):
        """
        post请求，参数在body中
        :param inerface_url:
        :param headerdata:
        :param interface_param:
        :return:
        """
        try:
            if interface_url != '':
                temp_interface_param = self.__new_params(interface_param)
                response = requests.post(url=interface_url, data=temp_interface_param, header=headerdata, verify=False,
                                         timeout=10)
                if response.status_code == 200:
                    durtime = (response.elapsed.microseconds) / 1000  # 发起请求和响应到达的时间，单位ms
                    result = {'code': '0000', 'message': '成功', 'data': response.text}
                else:
                    result = {'code': '2004', 'message': '接口返回状态错误', 'data': []}
            elif interface_url == '':
                result = {'code': '2002', 'message': '接口参数为空', 'data': []}

            else:
                result = {'code': '2003', 'message': '接口地址错误', 'data': []}
        except Exception as e:
            result = {'code': '9999', 'message': '系统异常', 'data': []}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def __http_get(self, interface_url, headerdata, interface_param):
        """
        get请求，参数放在url后面
        :param interface_url:
        :param headerdata: 请求头
        :param interface_param: 请求参数
        :return:
        """
        try:
            if interface_url != '':
                temp_interface_param = self.__new_params(interface_param)
                if interface_url.endswith('?'):
                    requrl = interface_url + temp_interface_param
                else:
                    requrl = interface_url + '?' + temp_interface_param
                response = requests.get(requrl, headers=headerdata, verify=False,
                                        timeout=10)  # verify参数是布尔类型，默认为True，即启动HTTPS的SSL证书验证
                print('response', response)
                if response.status_code == 200:
                    durtime = (response.elapsed.microseconds) / 1000
                    print('durtime', durtime)
                    result = {'code': '0000', 'message': '成功', 'data': response.text}
                else:
                    result = {'code': '3004', 'message': '接口返回状态错误', 'data': []}

            elif interface_url == '':
                result = {'code': '3002', 'message': '接口地址参数为空', 'data': []}
            else:
                result = {'code': '3003', 'message': '接口地址错误', 'data': []}
        except Exception as e:
            result = {'code': '9999', 'message': '系统异常', 'data': []}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def http_request(self, interface_url, headerdata, interface_param, request_type):
        """
        统一处理请求
        :param interface_url:
        :param headerdata:
        :param interface_param:
        :param request_type:
        :return:
        """
        try:
            if request_type == 'get' or request_type == 'GET':
                result = self.__http_get(interface_url, headerdata, interface_param)
            elif request_type == 'post' or request_type == 'POST':
                result = self.__http_post(interface_url, headerdata, interface_param)
            else:
                result = {'code': '1000', 'meaage': '请求类型错误', 'data': []}
        except Exception as e:
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result


if __name__ == '__main__':
    test_interface = RequestInterface()
    test_db = opmysql.OperationDbInterface(host_db='localhost', user_db='root', passed_db='123456',
                                           name_db='test_interface', port_db=3306, link_type=0)
    sen_sql = "select exe_mode,url_interface,header_interface,params_interface from case_interface" \
              " where name_interface = 'getIpInfo.php' and id=1"
    params_interface = test_db.select_one(sen_sql)
    print('返回数据：', str(params_interface))

    type_interface = params_interface['data']['exe_mode']
    print("exe_mode:", type_interface)
    if params_interface['code'] == '0000':
        url_interface = params_interface['data']['url_interface']
        temp = params_interface['data']['header_interface']
        print("请求头header:", temp)
        headerdata = eval(params_interface['data']['header_interface'])  # 转换成字典
        params_interface = params_interface['data']['params_interface']
        # type_interface = params_interface['data']['exe_mode']
        if url_interface != '' and headerdata != '' and params_interface != '' and type_interface != '':
            result = test_interface.http_request(interface_url=url_interface, headerdata=headerdata,
                                                 interface_param=params_interface, request_type=type_interface)
            print("result is :" ,result)
            if result['code'] == '0000':
                result_resp = result['data']
                print("处理http请求成功，返回数据是：%s" % result_resp)
            else:
                print("处理http请求失败")
        else:
            print("测试用例中有空值")
    else:
        print("获取测试用例数据失败")
