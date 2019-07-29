#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用于API认证的KEY
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
# 用于API认证的请求头
AUTH_KEY_NAME = 'auth-key'

# 错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASEDIR, "log", 'run.log')

# Agent模式保存服务器唯一ID的文件
CERT_FILE_PATH = os.path.join(BASEDIR, 'config', 'cert')

# 是否测试模式，测试模时候数据从files目录下读取
TEST_MODE = True

# 采集资产的方式，选项有：agent(默认), salt, ssh
MODE = 'ssh'

# 如果采用SSH方式，则需要配置SSH的KEY和USER
SSH_PRIVATE_KEY = "/root/.ssh/id_rsa"
SSH_USER = "root"
SSH_PORT = 22

# 采集硬件数据的插件
PLUGINS_DICT = {
    # 'cpu': 'src.plugins.cpu.CpuPlugin',
    # 'disk': 'src.plugins.disk.DiskPlugin',
    # 'main_board': 'src.plugins.main_board.MainBoardPlugin',
    # 'memory': 'src.plugins.memory.MemoryPlugin',
    # 'nic': 'src.plugins.nic.NicPlugin',
    'database': 'src.plugins.database.DatabasePlugin',
}

# 资产信息API
ASSET_API = "http://172.16.111.1:8000/api/asset"
# 数据库API
DATABASE_API = "http://172.16.111.1:8000/api/database"

SERVER_DATABASE_CONF = {
    'user': 'yang',
    'host': '172.16.111.131',
    'port': '3306',
    'password': '111111',
    'db': 'cmdb',
    'sql': 'select ip,port,db_name from cmdb.MysqlInfo'
}

CLIENT_DATABASE_CONF = {
    'user': 'yang',
    'host': '172.16.111.131',
    'port': '3306',
    'password': '111111',
    'sql_list': {'variables': 'show global variables;',
                 'status': 'show global status;',
                 'processlist': 'select user,host,db,time,info from information_schema.processlist where info is not null;',
                 'engine': 'show engine innodb status;',
                 },

}

SELECT_OPTIONS = ['database']   # 从server端收集数据库/服务器hostname(ip)的信息 ssh中 填写 'database'或 'asset'或者两者都填写

ASSET_AUTH_TIME = 2

"""
POST时，返回值：{'code': xx, 'message': 'xx'}
 code:
    - 1000 成功;
    - 1001 接口授权失败;
    - 1002 数据库中资产不存在
"""
