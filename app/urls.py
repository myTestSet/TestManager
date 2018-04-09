# -*- coding:utf-8 -*-

from django.conf.urls import url, include

urlpatterns = [
    url(r'account/', include('app.account.urls')),
    url(r'manager/', include('app.test_manager.urls')),
]