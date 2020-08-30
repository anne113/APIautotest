"""
定义对mysql数据库的操作
1.包括基本的单条语句的操作，删除，修改，更新
2.独立的查询单条，多条
3.独立的添加多条数据
"""

import logging

import MySQLdb
import pymysql

from public import config


class OperationDbInterface(object):
    def __init__(self, host_db='localhost', user_db='root', passed_db='123456', name_db='test_interface', port_db=3306,
                 link_type=0):
        """
        :param host_db:数据库主机
        :param user_db:数据库用户名
        :param passed_db:密码
        :param name_db:数据库模拟过程
        :param port_db:端口
        :param link_type:连接类型，用于输出的数据是元组还是字典，默认是字典，link_type=0
        :return:游标
        """
        try:
            if link_type == 0:
                self.conn = MySQLdb.connect(host=host_db,
                                            user=user_db,
                                            passwd=passed_db,
                                            db=name_db,
                                            port=port_db,
                                            charset='utf8'
                                            )
                # 创建数据库链接
                self.cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                # 返回字典
            else:
                self.cur = self.conn.cursor()
        except pymysql.Error as e:
            print("数据库链接失败 | mysql error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)

    def op_sql(self, condition):
        """
        定义单条数据操作，增加，删除，修改
        :param self:
        :param condition:sql语句，该通用方法可以用来替代insertone，updateone,deleteone
        :return:
        """
        try:
            self.cur.execute(condition)
            self.conn.commit()
            result = {'code': '0000', 'message': '执行通用操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行通用操作失败', 'data': []}
            print("数据库错误 | op_sql %d :%s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def select_one(self, condition):
        """
        返回单条数据
        :param self:
        :param condition: sql语句
        :return:字典形式的单条查询结果
        """
        try:
            row_affect = self.cur.execute(condition)
            if row_affect > 0:
                results = self.cur.fetchone()
                result = {'code': '0000', 'message': '执行单条查询成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行单条查询成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行单条查询异常', 'data': []}
            print("数据库执行错误 | select one %d : %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + "/log/syserror.",
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def select_all(self, condition):
        """
        查询表中多条数据
        :param self:
        :param condition:
        :return:
        """
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:  # 查询结果返回数据大于0
                self.cur.scroll(0, mode='absolute')  # 光标回到初始位置
                results = self.cur.fetchall()  # 返回游标中所有结果
                result_1 = {'code': "0000", 'message': '执行批量查询成功', 'data': results}
            else:
                result_1 = {'code': "0000", 'message': '执行批量查询成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result_1 = {'code': "9999", 'message': '执行批量查询异常', 'data': []}
            print("数据库错误 | select all  %d: %s".format(e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + "/log/syserror.log",
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result_1

    def insert_more(self, condition, params):
        """
        定义表中插入多条数据
        :param self:
        :param condition:
        :param params:
        :return:
        """
        try:
            results = self.cur.executemany(condition, params)  # 返回插入的数据条数
            self.conn.commit()
            result = {'code': "0000", 'message': '执行批量查询成功', 'data': int(results)}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': "9999", 'message': '执行批量查询异常', 'data': []}
            print("数据库错误 | insert more  %d: %s".format(e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + "/log/syserror.log",
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # def __del__(self):
    #     if self.cur != None:
    #         self.cur.close()
    #     if self.conn != None:
    #         self.conn.close()


if __name__ == '__main__':
    test = OperationDbInterface()
    sql = "select * from test_interface.config_total"
    result = test.select_all(sql)
    # result = test.select_one(sql)
    if result['code'] == '0000':
        print(result['data'])
    else:
        print(result['message'])
