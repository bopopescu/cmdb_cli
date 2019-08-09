#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-07-25 16:46
import traceback
import datetime
from utils.response import BaseResponse
from utils import agorithm
from repository import models

from django.db.models import Q
import datetime


# 读取数据库信息：然后循环传参给client，client执行sql，然后数据格式化，然后返回数据给server上

def get_untreated_database():
    response = BaseResponse()
    try:
        # 获取所有mha架构的数据库信息：
        result = models.MysqlInfo.objects.all().values('hostname', 'ip')
        response.data = list(result)
        response.status = True
        #
        # current_date = datetime.date.today()
        #
        # condition = Q()
        #
        # # 今日未采集的资产
        # con_date = Q()
        # con_date.connector = 'OR'
        # con_date.children.append(("asset__latest_date__lt", current_date))
        # con_date.children.append(("asset__latest_date", None))
        #
        # # 在线状态的服务器
        # con_status = Q()
        # con_status.children.append(('asset__device_status_id', '2'))
        #
        # condition.add(con_date, 'AND')
        # condition.add(con_status, 'AND')
        #
        # result = models.Server.objects.filter(condition).values('hostname')
        # response.data = list(result)
        # response.status = True
    except Exception as e:
        response.message = str(e)
        models.ErrorLog.objects.create(asset_obj=None, title='get_untreated_servers',
                                       content=traceback.format_exc())

    return response


class HandleMysql(object):
    @staticmethod
    def process(server_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            database_info = server_info['database']
            print(database_info)

            if not database_info['status']:
                response.status = False
                models.ErrorLog.objects.create(asset_obj=server_obj.asset, title='nic-agent', content=database_info['error'])
                return response

            client_mysql_dict = database_info['data']
            print(client_mysql_dict)
            mysql_obj_list = models.MysqlInfo.objects.filter(server_obj=server_obj)
            mysql_name_list = map(lambda x: x, (item.hostname for item in mysql_obj_list))

            update_list = agorithm.get_intersection(set(client_mysql_dict.keys()), set(mysql_name_list))
            add_list = agorithm.get_exclude(client_mysql_dict.keys(), update_list)
            del_list = agorithm.get_exclude(mysql_name_list, update_list)

            # 后面进行 接收数据模块 开发
            # HandleMysql._add_nic(add_list, client_mysql_dict, server_obj, user_obj)
            # HandleMysql._update_nic(update_list, mysql_obj_list, client_mysql_dict, server_obj, user_obj)
            # HandleMysql._del_nic(del_list, mysql_name_list, server_obj, user_obj)

        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(obj=server_obj.hostname, title='mysql-run', content=traceback.format_exc())
        return response

    @staticmethod
    def _add_nic(add_list, client_nic_dict, server_obj, user_obj):
        for item in add_list:
            cur_nic_dict = client_nic_dict[item]
            cur_nic_dict['name'] = item
            log_str = '[新增网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**cur_nic_dict)
            cur_nic_dict['server_obj'] = server_obj
            models.NIC.objects.create(**cur_nic_dict)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _del_nic(del_list, nic_objs, server_obj, user_obj):
        for item in nic_objs:
            if item.name in del_list:
                log_str = '[移除网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**item.__dict__)
                item.delete()
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _update_nic(update_list, nic_objs, client_nic_dict, server_obj, user_obj):

        for item in nic_objs:
            if item.name in update_list:
                log_list = []

                new_hwaddr = client_nic_dict[item.name]['hwaddr']
                if item.hwaddr != new_hwaddr:
                    log_list.append(u"[更新网卡]%s:mac地址由%s变更为%s" % (item.name, item.hwaddr, new_hwaddr))
                    item.hwaddr = new_hwaddr
                new_up = client_nic_dict[item.name]['up']
                if item.up != new_up:
                    log_list.append(u"[更新网卡]%s:状态由%s变更为%s" % (item.name, item.up, new_up))
                    item.up = new_up

                new_netmask = client_nic_dict[item.name]['netmask']
                if item.netmask != new_netmask:
                    log_list.append(u"[更新网卡]%s:掩码由%s变更为%s" % (item.name, item.netmask, new_netmask))
                    item.netmask = new_netmask

                new_ipaddrs = client_nic_dict[item.name]['ipaddrs']
                if item.ipaddrs != new_ipaddrs:
                    log_list.append(u"[更新网卡]%s:IP地址由%s变更为%s" % (item.name, item.ipaddrs, new_ipaddrs))
                    item.ipaddrs = new_ipaddrs

                item.save()
                if log_list:
                    models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj,
                                                      content=';'.join(log_list))


class HandleMHA(object):
    @staticmethod
    def process(server_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            nic_info = server_info['nic']
            if not nic_info['status']:
                response.status = False
                models.ErrorLog.objects.create(asset_obj=server_obj.asset, title='nic-agent', content=nic_info['error'])
                return response

            client_nic_dict = nic_info['data']
            nic_obj_list = models.NIC.objects.filter(server_obj=server_obj)
            nic_name_list = map(lambda x: x, (item.name for item in nic_obj_list))

            update_list = agorithm.get_intersection(set(client_nic_dict.keys()), set(nic_name_list))
            add_list = agorithm.get_exclude(client_nic_dict.keys(), update_list)
            del_list = agorithm.get_exclude(nic_name_list, update_list)

            HandleMHA._add_nic(add_list, client_nic_dict, server_obj, user_obj)
            HandleMHA._update_nic(update_list, nic_obj_list, client_nic_dict, server_obj, user_obj)
            HandleMHA._del_nic(del_list, nic_obj_list, server_obj, user_obj)

        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset_obj=server_obj.asset, title='nic-run', content=traceback.format_exc())

        return response

    @staticmethod
    def _add_nic(add_list, client_nic_dict, server_obj, user_obj):
        for item in add_list:
            cur_nic_dict = client_nic_dict[item]
            cur_nic_dict['name'] = item
            log_str = '[新增网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**cur_nic_dict)
            cur_nic_dict['server_obj'] = server_obj
            models.NIC.objects.create(**cur_nic_dict)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _del_nic(del_list, nic_objs, server_obj, user_obj):
        for item in nic_objs:
            if item.name in del_list:
                log_str = '[移除网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**item.__dict__)
                item.delete()
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _update_nic(update_list, nic_objs, client_nic_dict, server_obj, user_obj):

        for item in nic_objs:
            if item.name in update_list:
                log_list = []

                new_hwaddr = client_nic_dict[item.name]['hwaddr']
                if item.hwaddr != new_hwaddr:
                    log_list.append(u"[更新网卡]%s:mac地址由%s变更为%s" % (item.name, item.hwaddr, new_hwaddr))
                    item.hwaddr = new_hwaddr
                new_up = client_nic_dict[item.name]['up']
                if item.up != new_up:
                    log_list.append(u"[更新网卡]%s:状态由%s变更为%s" % (item.name, item.up, new_up))
                    item.up = new_up

                new_netmask = client_nic_dict[item.name]['netmask']
                if item.netmask != new_netmask:
                    log_list.append(u"[更新网卡]%s:掩码由%s变更为%s" % (item.name, item.netmask, new_netmask))
                    item.netmask = new_netmask

                new_ipaddrs = client_nic_dict[item.name]['ipaddrs']
                if item.ipaddrs != new_ipaddrs:
                    log_list.append(u"[更新网卡]%s:IP地址由%s变更为%s" % (item.name, item.ipaddrs, new_ipaddrs))
                    item.ipaddrs = new_ipaddrs

                item.save()
                if log_list:
                    models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj,
                                                      content=';'.join(log_list))


class HandleInstance(object):
    @staticmethod
    def process(server_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            nic_info = server_info['nic']
            if not nic_info['status']:
                response.status = False
                models.ErrorLog.objects.create(asset_obj=server_obj.asset, title='nic-agent', content=nic_info['error'])
                return response

            client_nic_dict = nic_info['data']
            nic_obj_list = models.NIC.objects.filter(server_obj=server_obj)
            nic_name_list = map(lambda x: x, (item.name for item in nic_obj_list))

            update_list = agorithm.get_intersection(set(client_nic_dict.keys()), set(nic_name_list))
            add_list = agorithm.get_exclude(client_nic_dict.keys(), update_list)
            del_list = agorithm.get_exclude(nic_name_list, update_list)

            HandleInstance._add_nic(add_list, client_nic_dict, server_obj, user_obj)
            HandleInstance._update_nic(update_list, nic_obj_list, client_nic_dict, server_obj, user_obj)
            HandleInstance._del_nic(del_list, nic_obj_list, server_obj, user_obj)

        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset_obj=server_obj.hostname, title='nic-run', content=traceback.format_exc())

        return response

    @staticmethod
    def _add_nic(add_list, client_nic_dict, server_obj, user_obj):
        for item in add_list:
            cur_nic_dict = client_nic_dict[item]
            cur_nic_dict['name'] = item
            log_str = '[新增网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**cur_nic_dict)
            cur_nic_dict['server_obj'] = server_obj
            models.NIC.objects.create(**cur_nic_dict)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _del_nic(del_list, nic_objs, server_obj, user_obj):
        for item in nic_objs:
            if item.name in del_list:
                log_str = '[移除网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**item.__dict__)
                item.delete()
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _update_nic(update_list, nic_objs, client_nic_dict, server_obj, user_obj):

        for item in nic_objs:
            if item.name in update_list:
                log_list = []

                new_hwaddr = client_nic_dict[item.name]['hwaddr']
                if item.hwaddr != new_hwaddr:
                    log_list.append(u"[更新网卡]%s:mac地址由%s变更为%s" % (item.name, item.hwaddr, new_hwaddr))
                    item.hwaddr = new_hwaddr
                new_up = client_nic_dict[item.name]['up']
                if item.up != new_up:
                    log_list.append(u"[更新网卡]%s:状态由%s变更为%s" % (item.name, item.up, new_up))
                    item.up = new_up

                new_netmask = client_nic_dict[item.name]['netmask']
                if item.netmask != new_netmask:
                    log_list.append(u"[更新网卡]%s:掩码由%s变更为%s" % (item.name, item.netmask, new_netmask))
                    item.netmask = new_netmask

                new_ipaddrs = client_nic_dict[item.name]['ipaddrs']
                if item.ipaddrs != new_ipaddrs:
                    log_list.append(u"[更新网卡]%s:IP地址由%s变更为%s" % (item.name, item.ipaddrs, new_ipaddrs))
                    item.ipaddrs = new_ipaddrs

                item.save()
                if log_list:
                    models.AssetRecord.objects.create(asset_obj=server_obj.asset, creator=user_obj,
                                                      content=';'.join(log_list))
