# from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor
# import time
# def task(arg):
#     print(arg)
#     time.sleep(1)
#
# # pool = ProcessPoolExecutor(5)
# pool = ThreadPoolExecutor(5)
#
# for i in range(50):
#     pool.submit(task,i)

from lib.response import BaseResponse
import pymysql
import re
from config import settings

from lib.serialize import Json

class GetServerDBInfo(object):
    '''
    获取server的cmdb数据库 table中数据库list
    '''
    response = BaseResponse()

    def __init__(self, user, host, port, passwd):
        self.user = user
        self.host = host
        self.port = port
        self.passwd = passwd

    def getinfo(self, sql, *args):
        dbinfo = None
        conn = pymysql.connect(host=self.host, user=self.user, port=self.port, password=self.passwd,
                               charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cur.execute(sql, args)
        if sql.find('select') >= 0 or sql.find('show') >= 0:
            dbinfo = cur.fetchall()
        else:
            conn.commit()
        cur.close()
        conn.close()
        if dbinfo:
            return dbinfo


class DatabasePlugin(object):
    def linux(self):
        response = BaseResponse()
        tmplist = {'database': {}}
        try:
            database_obj = GetServerDBInfo(user=settings.SERVER_DATABASE_CONF['user'],
                                           host=settings.SERVER_DATABASE_CONF['host'],
                                           port=int(settings.SERVER_DATABASE_CONF['port']),
                                           passwd=settings.SERVER_DATABASE_CONF['password'])

            ser_db_list = database_obj.getinfo(settings.SERVER_DATABASE_CONF['sql'], )
            # print(ser_db_list)

            for item in ser_db_list:
                l1 = []
                d1 = {}
                for subject in settings.CLIENT_DATABASE_CONF['sql_list']:
                    client_obj = GetServerDBInfo(user=settings.CLIENT_DATABASE_CONF['user'],
                                                 host=item['ip'],
                                                 port=item['port'],
                                                 passwd=settings.CLIENT_DATABASE_CONF['password'])
                    single = '{}_{}'.format(item['ip'], item['port'])
                    cli_db_info = client_obj.getinfo(settings.CLIENT_DATABASE_CONF['sql_list'][subject])

                    l1.append(cli_db_info)
                    # l1.append(cli_db_info[1])
                    d1[single] = l1

                tmplist["database"] = d1
            response.data = tmplist
        except Exception as e:
            print(e)

        return response


obj_1 = DatabasePlugin().linux()
print(obj_1.data)

print(Json.dumps(obj_1.data))
