#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-07-29 22:54

def ssh(cmd):
    import paramiko
    private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='172.16.111.131', port=22, username='root', pkey=private_key)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    ssh.close()
    print(result)
    return result


ssh('hostname')
