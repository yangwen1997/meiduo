from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from accounts.models import Acounts
from django.views.decorators.csrf import csrf_exempt
# 导入render和HttpResponse模块
from django.shortcuts import render, HttpResponse

# 导入Paginator,EmptyPage和PageNotAnInteger模块
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):

    return render(request,'accounts/index.html')

    # 展示账号数据
def account_list(request):
    '''
    website
    :param request:
    :return:
    '''
    website = request.GET.get('website',None)
    if website:
        query_list = Acounts.objects.filter(website=website)
        counts = query_list.count()
        # 生成paginator对象,定义每页显示10条记录
        paginator = Paginator(query_list, 15)
        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
        # 把当前的页码数转换成整数类型
        currentPage = int(page)
        try:
            query_list = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            query_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            query_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
        context = {'objs': query_list,'paginator':paginator,'website':website,'counts':counts}
        return render(request, 'accounts/accounts_list.html', context)
    query_list = Acounts.objects.all()
    context = {'objs':query_list}
    return render(request,'accounts/accounts_list.html',locals())


    # 增加账号
@csrf_exempt
def create(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        website = request.POST.get('website')
        counter = Acounts.objects.get(website__contains=website)
        account = Acounts.objects.create(phone=phone,password=password,website=website)
        return redirect("accounts:list")
    return render(request,'accounts/accounts_create.html')

    # 更新账号
def update(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        website = request.POST.get('website')
        obj = Acounts.objects.get(phone=phone)
        obj.password = password
        obj.website = website
        obj.save()
        return redirect("accounts:list")
    phone = request.GET.get('phone')
    obj = Acounts.objects.filter(phone=phone)
    context = {'obj':obj}
    return render(request,'accounts/accounts_update.html',context)

def delete(request):
    phone = request.GET.get('phone','')
    if phone:
        obj = Acounts.objects.filter(phone=phone)
        obj.delete()
        return redirect("accounts:list")

# 爬虫账号维护----------------------------------------------------------------
def create_accounts(request):
    '''
    创建账号
    :param request:
    :return:
    '''
    phone = request.GET.get('phone')
    password = request.GET.get('password')
    cookie = request.GET.get('cookie','')
    website = request.GET.get('website')
    if all([website,phone,password]):
        Acounts.objects.get_or_create(phone=phone,password=password,cookie=cookie,website=website)
        return HttpResponse('success')
    return HttpResponse("数据不全")

def get_all_accounts(request):
    '''
    返回列表包含账号 status == 1 的
    :param request:
    :return:
    '''
    website = request.GET.get('website')
    query_set = Acounts.objects.filter(website=website)
    json_data = serializers.serialize("json", query_set)
    return HttpResponse(json_data,content_type="application/json")

def get_goood_acounts(request):
    '''
    返回列表包含账号 status == 1 的
    :param request:
    :return:
    '''
    website = request.GET.get('website')
    query_set = Acounts.objects.filter(status=0,website=website)
    json_data = serializers.serialize("json", query_set)
    return HttpResponse(json_data,content_type="application/json")

def get_bad_acounts(request):
    '''
    获取被ban的账号
    :param request:
    :return:
    '''
    website = request.GET.get('website')
    query_set = Acounts.objects.filter(status=1,website=website)
    json_data = serializers.serialize("json", query_set)
    return HttpResponse(json_data, content_type="application/json")

def update_things(request):
    '''
    更新状态
    :param request:
    :return:
    '''
    phone = request.GET.get('phone')
    status=request.GET.get('status',None)
    cookie = request.GET.get('cookie',None)
    trouble = request.GET.get('trouble',None)
    website = request.GET.get('website')
    baned = request.GET.get('baned',False)
    obj = Acounts.objects.filter(phone=phone,website=website)
    if obj.count()>0:
        if trouble:
            obj.update(trouble=trouble,baned=True)
        if cookie:
            obj.update(cookie=cookie,baned=False)
        if status:
            obj.update(status=status)
        return HttpResponse('success')
    return HttpResponse('没找到该账号')



def recovery_all_accounts(request):
    '''
    重置所有的cookie
    :param request: 网站名字
    :return:
    '''
    website = request.GET.get('website')
    query_set = Acounts.objects.filter(website=website).update(status=0)
    json_data = serializers.serialize("json", query_set)
    return HttpResponse(json_data, content_type="application/json")

def delete_accounts(request):
    '''
    删除账号
    :param request:
    :return:
    '''
    phone = request.GET.get('phone')
    if phone:
        obj = Acounts.objects.filter(phone=phone)
        obj.delete()
        return HttpResponse('success')
