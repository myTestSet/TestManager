# -*- coding:utf-8 -*-

from django.conf.urls import url, include

urlpatterns = [
    url(r'account/', include('app.account.urls')),
    url(r'manager/', include('app.test_manager.urls')),
    url(r'activity/', include('app.activity_set.urls')),
    url(r'util/', include('app.test_util.urls')),
]