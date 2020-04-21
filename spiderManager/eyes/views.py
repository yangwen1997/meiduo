import json
import time
from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from eyes.models import Host
from pymongo import MongoClient


now = lambda :'%.0f'%time.time()

client = MongoClient(settings.IP_MONGO_URI)
def data_handle(name,couser):
    instance = []
    for c in couser:
        datas = c['doc']
        for data in datas:
            t = data['updateTime']
            t = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
            seconds = float(now())-t
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            data['distance'] = "%02d:%02d:%02d" % (h, m, s)
            instance.append(data)
        return {"name":name,'data':instance}

def handle(request):
    global client
    h_col = client[settings.DB][settings.HCOL]
    a_col = client[settings.DB][settings.ACOL]
    # db.getCollection('hui_ip_results').aggregate([{"$group" : {"_id" : null, "doc" : {"$push":{'ip':"$ip",'mac':'$mac','updateTime':'$updateTime'}}}}])
    container = []
    hcol_data = h_col.aggregate([{"$group" : {"_id" : None, "doc" : {"$push":{'ip':"$port",'mac':'$mac','updateTime':'$updateTime'}}}}])
    acol_data = a_col.aggregate([{"$group" : {"_id" : None, "doc" : {"$push":{'ip':"$port",'mac':'$mac','updateTime':'$updateTime'}}}}])
    container.append(data_handle('单独拨号',hcol_data))
    container.append(data_handle('全部拨号',acol_data))

    response = HttpResponse(json.dumps(container))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
