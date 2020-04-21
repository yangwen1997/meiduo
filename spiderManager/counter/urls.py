# -*- coding: utf-8 -*-

from django.conf.urls import url
from counter.views import get_data,data_handler,charts,chartData,sum_day,typesAll
from django.views.generic.base import TemplateView 

urlpatterns = [
    url(r'^data_handler',data_handler,name='handler'),
    url(r'^today$',get_data,name='today'),
    # url(r'^show$',charts,name='show'),
    url(r'^show$',TemplateView.as_view(template_name='counter/ajax.html'),name='show'),
    url(r'^ajax$',chartData,name='json'),
    url(r'^sum_day',sum_day,name='sum_day'),
    url(r'^types',typesAll,name='types'),
]
