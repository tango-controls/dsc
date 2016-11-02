# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from dsc.views import DeviceServerDetailView, DeviceServerAddView

from tango.cms_urls import content_action_urls #TODO do przemyślenia i implementacji w DSc potrzebne akcje albo kopia i włąśne

urlpatterns = patterns(
    '',
    # url(
    #     r'^/$',
    #     DeviceServerListView.as_view(),
    #     name='deviceserver_list'),

    url(
         r'^ds/(?P<pk>.*)/$',
         DeviceServerDetailView.as_view(),
         name='deviceserver_detail'),

    url(
         r'^add/$',
         DeviceServerAddView.as_view(),
         name='deviceserver_add'),
)

