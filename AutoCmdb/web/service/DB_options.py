#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-08-01 17:20

import os
import traceback
import pymysql


class GetServerDBInfo(object):
    '''
    获取server的cmdb数据库 table中数据库list
    '''

    def __init__(self, user, host, port, passwd):
        self.user = user
        self.host = host
        self.port = port
        self.passwd = passwd

    def getinfo(self, sql, *args):
        print(args[0])
        dbinfo = None
        conn = pymysql.connect(host=self.host, user=self.user, port=self.port, password=self.passwd,
                               charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        if len(args) > 0:
            cur.execute(sql, args[0])
        else:
            cur.execute(sql, [])
        if sql.find('select') >= 0 or sql.find('show') >= 0:
            dbinfo = cur.fetchall()
        else:
            conn.commit()
        cur.close()
        conn.close()
        if dbinfo:
            return dbinfo
