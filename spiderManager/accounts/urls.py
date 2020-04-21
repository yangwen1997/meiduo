# _*_coding:utf-8_*_

from django.conf.urls import url
from accounts.views import (index,account_list,create,delete,update,
                            get_goood_acounts,get_all_accounts,
                            get_bad_acounts,update_things,
                            recovery_all_accounts,delete_accounts,
                            create_accounts)

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^list$',account_list, name='list'),
    url(r'^create$',create,name='create'),
    url(r'^update$',update,name='update'),
    url(r'^delete$',delete,name='delete'),
    url(r'^delete$',delete,name='delete'),
    # cookie维护--------------------------------------------
    url(r'^create_accounts',create_accounts,name='create_accounts'),
    url(r'^get_good_accounts',get_goood_acounts,name='get_good_accounts'),
    url(r'^get_bad_accounts',get_bad_acounts,name='get_bad_accounts'),

    url(r'^recovery_all_accounts',recovery_all_accounts,name='recovery_all_accounts'),
    url(r'^delete_accounts',delete_accounts,name='delete_accounts'),
    url(r'^get_all_accounts',get_all_accounts,name='get_all_accounts'),
    url(r'^update_things',update_things,name='update_things'),

]