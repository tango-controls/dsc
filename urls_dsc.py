# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from dsc.views import (
    DeviceServerDetailView, DeviceServerListView, DeviceServerActionView,
)
from tango.cms_urls import content_action_urls #TODO do przemyślenia i implementacji w DSc potrzebne akcje albo kopia i włąśne

urlpatterns = patterns(
    '',
    url(
        r'^dsc/$',      #TODO delete dsc as the view will be in cms plugin content on device_server_catalogue site
        DeviceServerListView.as_view(),
        name='device_server_list'),

    # TODO dodać content actions view
    url(
         r'^dsc/(?P<slug>[\w-]+)/$',
         DeviceServerDetailView.as_view(),
         name='device_server_detail'),
)

'''
TEST PIOTRA
urlpatterns = [
    url(r'^dsc/$', views.index, name='dsc_index'),
    url(r'^dsc/ds/(?P<device_server_id>.*)$', views.device_server_detail, name='device_server__detail')
]
'''


'''url(
    r'^(?P<slug>[\w-]+)/', include(
        [
            url(r'^$',
                DeviceServerDetailView.as_view(),
                name='device_server__detail'),
        ] + content_action_urls(DeviceServerActionView),
    ),
)'''
