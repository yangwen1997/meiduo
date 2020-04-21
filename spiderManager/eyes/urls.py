# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import TemplateView

from eyes.views import handle

urlpatterns = [
    # url(r'^data_handler',data_handler,name='handler'),
    # url(r'^today$',get_data,name='today'),
    url(r'^ajax$',handle,name='handler'),
    url(r'^',TemplateView.as_view(template_name="eyes/chart.html")),
    ]