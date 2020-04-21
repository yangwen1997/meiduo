import datetime
import json

from django.core import serializers
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from counter.models import Counter,Types,SumNum
from django.views.decorators.csrf import csrf_exempt
# 获取当天的数据.
def get_data(request):
    date = datetime.date.today()
    data = Counter.objects.filter(timestamp=date)
    json_data = serializers.serialize("json", data)
    return HttpResponse(json_data, content_type="application/json")

# 保存数据到数据库
@csrf_exempt
def data_handler(request):
    data_number = request.POST.get('number')
    collection = request.POST.get('collection')
    types = request.POST.get('type')
    # 种类
    t = Types.objects.get(name=types)
    name = request.POST.get('name')
    date = datetime.date.today()
    # time = time.strftime("%H:%M:%S")
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    before_numbers = Counter.objects.filter(timestamp=today, name=name).order_by('-id').first()

    if before_numbers is None:
        before_numbers =  Counter.objects.filter(name=name).order_by('-id').first()
        if before_numbers:
            before_numbers = before_numbers.number
        else:
            before_numbers=0
    else:
        before_numbers = before_numbers.number
    record = int(data_number)-before_numbers
    ret = Counter.objects.create(timestamp=date,number=data_number,name=name,collection=collection,record=record,typec=t)

    return JsonResponse({'status':'success'})


def charts(request):
    '''
    表单显示
    :param request:
    :return:
    '''
    name= request.GET.get('name',None)
    seven_days  = datetime.timedelta(days=7)
    today = datetime.date.today()
    that_day = today-seven_days
    all = Counter.objects.filter(timestamp__range=(that_day, today))
    names = Counter.objects.all().distinct().values('name')
    if name:
        name=name
    else:
        name = names.first()['name']
    # -------------今天的数据--------------------
    #print(name)
    try:
        tdata = all.filter(name=name,timestamp=today).order_by('-time').first().number
    except:
        tdata=0
   # print(tdata)
    # -------------获取昨天的数据-----------------
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    yestody_number = Counter.objects.filter(timestamp=yesterday,name=name).order_by('-time').first()
    if yestody_number is None:
        ydata = 0
    else:
        ydata = yestody_number.number
    # -------------------------------------------
    datas = all.filter(name=name)
    instance = []
    for item in datas:
        ret = item.get_time_number()
        instance.append(ret)
    updata= tdata-ydata
    context={'names':names,"data":instance,'cname':name,'tdata':tdata,'ydata':ydata,'updata':updata}
    return render(request,'counter/charts.html',context=context)

# ajax 接口
def chartData(request):
        name = request.GET.get('name')
        if name !=None:
            name = request.GET.get('name', None)
            seven_days = datetime.timedelta(days=7)
            today = datetime.date.today()
            that_day = today - seven_days
            all = Counter.objects.filter(timestamp__range=(that_day, today))

            names = Counter.objects.all().distinct().values('name')
            if name:
                name = name
            else:
                name = names.first()['name']
            # -------------今天的数据--------------------
            # print(name)
            try:
                tdata = all.filter(name=name, timestamp=today).order_by('-time').first().number
            except:
                tdata = 0
            # -------------获取昨天的数据-----------------
            oneday = datetime.timedelta(days=1)
            yesterday = today - oneday
            yestodays =  Counter.objects.filter(timestamp=yesterday, name=name)
            yestody_number =yestodays.order_by('-time').first()
            if yestody_number is None:
                ydata=0
                ysum = 0
            else:
                ydata = yestody_number.number
                ysum = yestodays.aggregate(Sum('record'))['record__sum']
            # -------------------------------------------
            datas = all.filter(name=name)

            instance = []
            for item in datas:
                ret = item.get_time_number()
                instance.append(ret)
            updata = tdata - ydata

            data = {"data": instance,
                    'cname': name,
                    'tdata': tdata,
                    'ydata': ydata,
                    'updata': updata,
                    'ysum':ysum
                    }
            response = HttpResponse(json.dumps(data))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response

def sum_day(request):
    # 查询总量数据库 返回json
    days = datetime.timedelta(days=360)
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    that_day = today - days
    datas = SumNum.objects.filter(date__range=(that_day, today)) 
    container = []
    
    for data in datas:
        if data.typec.name=='其他':
           continue
        dic = {}
        dic['number'] = data.number
        dic['type'] = data.typec.name
        dic['date'] = data.date.strftime("%Y-%m-%d")

        container.append(dic)
    response = HttpResponse(json.dumps(container))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def typesAll(request):
    # 分类的总数
    types_all_counters = []
    ts = Types.objects.all()
    for i in ts:
        # print(i.id, i.name)
        if i.name=="其他":
            continue
        names = Counter.objects.filter(typec_id=i.id).distinct().values('name')
        _all_sum = 0
        for name in names:
            
            a = Counter.objects.filter(name=name['name']).order_by('-id').first()
            # print(a.number)
            _all_sum += a.number
        # print("--------------")
        # print(_all_sum)
        data = {i.name: _all_sum}
        types_all_counters.append(data)

    response = HttpResponse(json.dumps(types_all_counters))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
