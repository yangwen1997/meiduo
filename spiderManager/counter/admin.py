from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.admin import helpers
from counter.models import Counter,Types,SumNum


class CounterAdmin(admin.ModelAdmin):

    list_display = ['name','collection','number','typec']
    list_filter = ['name','collection','typec']
    search_fields = ['name','collection','typec']
    fields = ('name','typec')
    actions = ['updateName','updateCol']

    def updateName(self, request, queryset):
        if request.POST.get('new_name'):
            name = request.POST.get("new_name")
            queryset.update(name=name)
        else:
            context = {
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'action':'updateName'
            }
            return TemplateResponse(request, '../templates/middle.html', context=context)

    def updateCol(self, request, queryset):
        if request.POST.get('new_name'):
            name = request.POST.get("new_name")
            queryset.update(collection=name)
        else:
            context = {
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'action':'updateCol'
            }
            return TemplateResponse(request, '../templates/middle.html', context=context)

class SumAdmin(admin.ModelAdmin):
    list_display=['number','date','typec']
    fields = ['number','date']
admin.site.register(Counter,CounterAdmin)
admin.site.register(Types)
admin.site.register(SumNum,SumAdmin)
