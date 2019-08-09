#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-07-30 19:01


import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList


class Grant(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'db_name', 'text': '数据库名', 'condition_type': 'input'},
            {'name': 'db_ip', 'text': 'IP', 'condition_type': 'input'},
            {'name': 'request_user', 'text': '申请人', 'condition_type': 'input'},
            {'name': 'description', 'text': '唯一标识', 'condition_type': 'input'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 0,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}  # 自定义属性
            },
            {
                'q': 'request_user',
                'title': "申请人",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@request_user'}},
                'attr': {'name': 'request_user', 'id': '@request_user', 'origin': '@request_user'}
            }, {
                'q': 'description',
                'title': "描述",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@description'}},
                'attr': {'name': 'description', 'id': '@description', 'origin': '@description'}
            },
            {
                'q': 'db_username',
                'title': "用户名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@db_username'}},
                'attr': {'name': 'db_username', 'id': '@db_username', 'origin': '@db_username'}
            },
            {
                'q': 'db_name',
                'title': "库名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@db_name'}},
                'attr': {'name': 'db_name', 'id': '@db_name', 'origin': '@db_name'}
            }, {
                'q': 'db_ip',
                'title': "IP",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@db_ip'}},
                'attr': {'name': 'db_ip', 'id': '@db_ip', 'origin': '@db_ip'}
            }, {
                'q': 'port',
                'title': "Port",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@port'}},
                'attr': {'name': 'port', 'id': '@port', 'origin': '@port'}
            }, {
                'q': 'host_ip',
                'title': "被授权IP",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@host_ip'}},
                'attr': {'name': 'host_ip', 'id': '@host_ip', 'origin': '@host_ip'}
            }, {
                'q': 'db_permission',
                'title': "权限",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@db_permission'}},
                'attr': {'name': 'db_permission', 'id': '@db_permission', 'origin': '@db_permission'}
            }, {
                'q': 'status',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@status'}},
                'attr': {'name': 'status', 'id': '@status', 'origin': '@status'}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<button type='button'  onclick='grant_agree(this)' nid='{nid}' class='btn btn-success btn-xs'>通过</button> <button type='button' onclick='grant_refuse(this)' nid='{nid}' class='btn btn-danger btn-xs'>拒绝</button>",'kwargs': {'nid': '@id'}},
                'attr': {}
            }
        ]
        # 额外搜索条件
        extra_select = {}
        super(Grant, self).__init__(condition_config, table_config, extra_select)

    def fetch_grant(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)

            asset_count = models.DBGrantHistory.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)

            asset_list = models.DBGrantHistory.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {}
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_grant(request):
        # pass
        response = BaseResponse()
        # try:
        #     delete_dict = QueryDict(request.body, encoding='utf-8')
        #     id_list = delete_dict.getlist('id_list')
        #     models.MysqlInitInfo.objects.filter(id__in=id_list).delete()
        #     response.message = '删除成功'
        #     pass
        # except Exception as e:
        #     response.status = False
        #     response.message = str(e)
        return response

    @staticmethod
    def put_grant(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                    models.DBGrantHistory.objects.filter(id=nid).update(**row_dict)
                except Exception as e:
                    response.error.append({'num': num, 'message': str(e)})
                    response.status = False
                    error_count += 1
            if error_count:
                response.message = '共%s条,失败%s条' % (len(update_list), error_count,)
            else:
                response.message = '更新成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def grant_detail(db_name, db_id):
        response = BaseResponse()
        try:
            response.data = models.DBGrantHistory.objects.filter(id=db_id, name=db_name).first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
