#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from .base import BasePlugin
from lib.response import BaseResponse
from config import settings


class BasicPlugin(BasePlugin):
    def os_platform(self):
        """
        获取系统平台
        :return:
        """
        if self.test_mode:
            output = 'linux'
        else:
            # output = self.exec_shell_cmd('uname')
            output = 'linux'
        return output.strip()

    def os_version(self):
        """
        获取系统版本
        :return:
        """
        if self.test_mode:
            output = """CentOS release 6.6 (Final)\nKernel \r on an \m"""
        else:
            # output = self.exec_shell_cmd('cat /etc/issue')
            output = """CentOS release 6.6 (Final)\nKernel \r on an \m"""
        result = output.strip().split('\n')[0]
        return result

    def os_hostname(self):
        """
        获取主机名
        :return:
        """
        if self.test_mode:
            output = 'c1.com'
        else:
            # hostname = self.exec_shell_cmd('hostname')
            # print(hostname)
            # hostname = '5e6348bc3336'
            from src.plugins.database import GetServerDBInfo
            database_obj = GetServerDBInfo(user=settings.SERVER_DATABASE_CONF['user'],
                                           host=settings.SERVER_DATABASE_CONF['host'],
                                           port=int(settings.SERVER_DATABASE_CONF['port']),
                                           passwd=settings.SERVER_DATABASE_CONF['password'])
            tmp_result = database_obj.getinfo(
                'select ip,hostname from cmdb_mha.MysqlInfo where hostname = %s', [self.hostname])
            output = tmp_result[0]['ip']

        return output.strip()

    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'os_platform': self.os_platform(),
                'os_version': self.os_version(),
                'hostname': self.os_hostname(),
            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response
