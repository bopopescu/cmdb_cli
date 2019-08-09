#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-07-30 20:41

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from repository import models
import json


from web.service import backup


class BackupListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'backup_list.html')


class BackupJsonView(View):
    def get(self, request):
        obj = backup.Backup()
        response = obj.fetch_backup(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = backup.Backup.delete_backup(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = backup.Backup.put_backup(request)
        return JsonResponse(response.__dict__)


class BackupDetailView(View):
    def get(self, request, db_name, db_id):
        response = backup.Backup.backup_detail(db_name, db_id)
        return render(request, 'database_detail.html', {'response': response, 'db_name': db_name})


class AddBackupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_backup.html')

    def post(self, request, *args, **kwargs):
        ret = {"status": True, "msg": ""}
        add_info = request.POST
        a = json.dumps(add_info)
        try:
            models.BackupInfo.objects.create(**json.loads(a))
        except Exception as e:
            print(e)
            ret = {"status": False, "msg": e}
        return JsonResponse(ret)
