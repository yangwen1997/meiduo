# -*- coding: utf-8 -*-
import datetime
import os
import django
# # set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiderManager.settings')
# Setup django project
django.setup()

today = datetime.date.today()
oneday = datetime.timedelta(days=1)
twoday = datetime.timedelta(days=2)
yesterday = today - oneday
beforeday = today - twoday
from counter.models import Counter

names = Counter.objects.all().distinct().values('name')
for n in names:
    data = Counter.objects.filter(name=n['name'],timestamp=yesterday)
    for ind in range(len(data)-1):
        record =data[ind+1].number - data[ind].number
        _id = data[ind+1].id
        print(record,_id)
        Counter.objects.filter(id=_id).update(record=record)



