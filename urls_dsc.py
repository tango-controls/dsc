# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from dsc.views import DeviceServerDetailView, DeviceServerAddView
from django.contrib.auth.decorators import login_required, permission_required

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
         r'^ds/(?P<pk>.*)/update/$',
         permission_required('dsc.change_deviceserver')(DeviceServerDetailView.as_view()),
         name='deviceserver_update'),

    url(
         r'^ds/(?P<pk>.*)/verify/$',
         permission_required('dsc.admin_deviceserver')(DeviceServerDetailView.as_view()),
         name='deviceserver_verify'),

    url(
         r'^add/$',
         permission_required('dsc.add_deviceserver')(DeviceServerAddView.as_view()),
         name='deviceserver_add'),
)

