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

yesterday = today - oneday

from counter.models import Counter

names = Counter.objects.all().distinct().values('name')
for n in names:
    c_data = Counter.objects.filter(timestamp=today,name=n['name']).first()
    if c_data is not None:
        b_data = Counter.objects.filter(timestamp=yesterday, name=n['name']).last()
        if b_data is None:
            continue
        print("前提",b_data,b_data.number,b_data.time," | ","昨天",c_data,c_data.number,c_data.time)
        _id = c_data.id
        r = c_data.number - b_data.number
        Counter.objects.filter(id=_id).update(record=r)
        print(Counter.objects.get(id=_id).record)
    else:
        print(n['name'])
