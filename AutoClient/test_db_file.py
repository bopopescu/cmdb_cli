#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-07-26 10:10


import json
from lib.response import BaseResponse
from files import database

response = BaseResponse()

# response.data = database.datainfo
# for item in response.data['database']:
#     for i in response.data['database'][item]:
#         print(i)


print(json.dumps(database.datainfo))


