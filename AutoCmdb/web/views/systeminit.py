#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-08-05 14:58

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from utils import ssh_client
from web.service import chart
import json
from web.conf import config
from repository import models
import paramiko
import os

from web.service import system
from concurrent.futures import ThreadPoolExecutor


class SystemInitListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'system_list.html')


class SystemInitJsonView(View):
    def get(self, request):
        obj = system.System()
        response = obj.fetch_system(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = system.System.delete_system(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = system.System.put_system(request)
        return JsonResponse(response.__dict__)


class SystemAddView(View):
    def __init__(self):
        self.fun_dict = {'copy_software': self.copy_software, "send_ssh_auth_mha": self.send_ssh_auth_mha}

    def send_ssh_auth_mha(self, host_list):
        '''
        将秘钥传输到host_list机器上
        :param host:
        :return:
        '''

    def copy_software(self, host):
        '''
        scp 传输数据到host 主机上
        :return:
        '''
        os.system('/bin/bash /system_init/software/push_ssh.sh')
        os.system('scp /data/software/mysql_init/ %s:/data/software/mysql_init/' % (host))
        ssh = ssh_client.MyParamikoClient()
        command = 'sh -x /system_init/software/mysql_system_init.sh'
        status_code, content = ssh.run(host, command)
        return status_code, content

    def system_init(self):
        tmplist = models.SystemRecord.objects.filter(id='').values('hostname', 'ip')
        with open('/system_init/software/sshlist.txt', 'w', encoding='utf8') as f:
            pool = ThreadPoolExecutor(10)
            for item in tmplist:
                pool.submit(self.copy_software, item['ip'])
                f.write(item['ip'])
                f.write('\n')
            # 此处通过线程池来执行
            pool.shutdown(wait=True)

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'msg': ''}
        add_info = request.POST
        add_dict = json.loads(json.dumps(add_info))

        try:

            # 此处要实现异步远程执行数据同步，并初始化数据库环境
            # 拷贝数据文件，脚步到目标机器
            ret = {'status': True, 'msg': '申请成功'}
            models.SystemRecord.objects.create(**add_dict)
        except Exception as e:
            print(e)
            ret = {"status": False, "msg": "授权失败"}
        return JsonResponse(ret)
