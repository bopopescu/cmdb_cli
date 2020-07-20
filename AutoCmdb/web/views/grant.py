#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-07-30 20:41

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from repository import models
import json, datetime
from AutoCmdb import settings
from django.http.request import QueryDict
import paramiko, pymysql

from web.service import grant


class GrantListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'grant_list.html')


class GrantJsonView(View):
    def get(self, request):
        obj = grant.Grant()
        response = obj.fetch_grant(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = grant.Grant.delete_grant(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = grant.Grant.put_grant(request)
        return JsonResponse(response.__dict__)


class AddGrantView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_grant.html')

    def post(self, request, *args, **kwargs):
        ret = {"status": True, "msg": ""}
        add_info = request.POST
        add_dict = json.loads(json.dumps(add_info))
        try:
            models.DBGrantHistory.objects.create(**add_dict)
        except Exception as e:
            ret = {"status": False, "msg": "授权失败"}
        return JsonResponse(ret)

    def grant_option(self, *args, **kwargs):
        print(args)
        # db_ip, db_port, db_name, grant_ip, grant_user, grant_password, grant_limit = ()


class GrantDefineView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'grant_list.html')

    def post(self, request, *args, **kwargs):
        ret = {"status": True, "msg": ""}
        if request.POST:
            grant_info = request.POST
            grant_dict = json.loads(json.dumps(grant_info))

            try:
                define_result = models.MysqlInfo.objects.filter(**grant_dict)
                if define_result:
                    ret = {"status": True, "msg": "数据库存在"}
                else:
                    ret = {"status": False, "msg": ""}
            except Exception as e:
                print(e)
                ret = {"status": False, "msg": "请联系管理员"}
            return JsonResponse(ret)


class GrantAgreeView(View):
    def put(self, request, *args, **kwargs):
        ret = {'status':True,'msg':'',}
        put_dict = QueryDict(request.body, encoding='utf-8')
        update_list = json.loads(json.dumps(put_dict))
        error_count = 0
        for i in put_dict:
            grant_status = models.DBGrantHistory.objects.filter(id=i).values('status')
            print(grant_status[0])
            if grant_status[0]['status'] != '待审批':
                # 已授权，已拒绝
                ret[i] = True
            else:
                ret[i] = False

        return JsonResponse(ret)



    def post(self, request, *args, **kwargs):
        ret = {'status': False, 'msg': '授权错误，联系管理员'}
        opt_dict = request.POST
        only_info = json.loads(json.dumps(opt_dict))
        '''
        {'request_user': 'yang2', 'description': '1', 'db_name': 'cmdb_mha', 'db_ip': '172.16.111.131', 'port': '3306', 'host_ip': '10.0.0.1','db_permission': 'RO', 'status': '待审批'}
        1. 检查IP，端口的主从信息
        2. 检查授权历史库中是否已经再次授权
        '''
        role_obj = models.MysqlInfo.objects.filter(db_name=only_info['db_name'], ip=only_info['db_ip'],
                                                   port=only_info['port']).values('ip', 'role', 'port', 'main_ip',
                                                                                  'main_port')
        if role_obj[0]['role'] != 'main':
            role_obj['ip'] = role_obj['main_ip']
            role_obj['port'] = role_obj['main_port']

        grant_his_obj = models.DBGrantHistory.objects.filter(db_name=only_info['db_name'], db_ip=only_info['db_ip'],
                                                             port=only_info['port'])
        grant_his_dict = grant_his_obj.values('db_username', 'db_password')
        print(grant_his_dict[0])
        if grant_his_obj:
            '''
            如果不支持使用单一账号链接所有数据库，此处需要使用ssh/salt等方式+秘钥链接到数据库主机，进行执行mysql命令判断+授权
            远程链接到数据库上执行命令
                1.检查远程库上有无此账号.
            '''
            from web.service.DB_options import GetServerDBInfo
            mysql_option = GetServerDBInfo(user=settings.DB_USER, passwd=settings.DB_PASS, host=role_obj[0]['ip'],
                                           port=role_obj[0]['port'])
            his_sql = 'select user,host from mysql.user where user=%s and host=%s;'
            his_result = mysql_option.getinfo(his_sql, [only_info['db_username'], only_info['host_ip']])
            if his_result:
                ret = {'status': False, 'msg': '账号已存在'}
            else:
                '''远程操作数据库授权'''
                try:
                    if only_info['db_permission'] == 'RO':
                        '''申请只读权限'''
                        grant_sql = 'grant select on %s.* to "%s"@"%s" identified by "%s";' % (
                        only_info['db_name'], grant_his_dict[0]['db_username'], only_info['host_ip'],
                        grant_his_dict[0]['db_password'])
                    elif only_info['db_permission'] == 'RW':
                        grant_sql = 'grant select, delete, insert, update on %s.* to "%s"@"%s" identified by "%s";' % (
                        only_info['db_name'], grant_his_dict[0]['db_username'], only_info['host_ip'],
                        grant_his_dict[0]['db_password'])
                    else:
                        grant_sql = 'grant select on %s.* to "%s"@"%s" identified by "%s";' % (
                        only_info['db_name'], grant_his_dict[0]['db_username'], only_info['host_ip'],
                        grant_his_dict[0]['db_password'])
                        ret = {'status': False, 'msg': '权限有问题，请联系管理员'}

                    mysql_option = GetServerDBInfo(user=settings.DB_USER, passwd=settings.DB_PASS,
                                                   host=role_obj[0]['ip'], port=role_obj[0]['port'])
                    mysql_option.getinfo(grant_sql, [])
                    # mysql_option.getinfo(grant_sql, [only_info['db_name'], grant_his_dict[0]['db_username'], only_info['host_ip'], grant_his_dict[0]['db_password']])

                    # mysql_option = GetServerDBInfo(user=settings.DB_USER, passwd=settings.DB_PASS,
                    #                                host=role_obj[0]['ip'],
                    #                                port=role_obj[0]['port'])
                    # mysql_option.getinfo('flush privileges;',[])
                    grant_his_obj.update(operation_user='dba', status='以授权')
                    ret = {'status': True, 'msg': '授权成功'}
                except Exception as e:
                    print(e)
                    ret = {'status': False, 'msg': '授权失败，请联系管理员'}

        return JsonResponse(ret)
