#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-08-07 11:05

import paramiko


class MyParamikoClient(object):

    def run(self, host, command):  # /root/.ssh/id_rsa
        private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
        transport = paramiko.Transport((host, 22))  # 这难道可以试试多个机器？
        transport.connect(username='devops', pkey=private_key)

        ssh = paramiko.SSHClient()
        ssh._transport = transport

        stdin, stdout, stderr = ssh.exec_command(command)

        if stdout:
            status_code = 0
            content = stdout.read()
        else:
            status_code = 1
            content = stderr.read()

        transport.close()
        return status_code, content
