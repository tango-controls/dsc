# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from dsc.views import DeviceServerDetailView, DeviceServerAddView, search_view, \
    DeviceServerManufacturerAutocomplete, DeviceServerProductAutocomplete, \
    DeviceServerFamilyAutocomplete,DeviceServerLicenseAutocomplete, DeviceServerBusAutocomplete, \
    DeviceServerUpdateView
from django.contrib.auth.decorators import login_required, permission_required

from tango.cms_urls import content_action_urls #TODO do przemyślenia i implementacji w DSc potrzebne akcje albo kopia i włąśne

urlpatterns = patterns(
    '',
    # url(
    #     r'^/$',
    #     DeviceServerListView.as_view(),
    #     name='deviceserver_list'),

    url(
         r'^ds/(?P<pk>\d+)/update/$',
         DeviceServerUpdateView.as_view(),
         name='deviceserver_update'),

    url(
         r'^ds/(?P<pk>.*)/verify/$',
         permission_required('dsc.admin_deviceserver')(DeviceServerDetailView.as_view()),
         name='deviceserver_verify'),

    url(
         r'^ds/(?P<pk>.*)/$',
         DeviceServerDetailView.as_view(),
         name='deviceserver_detail'),

    url(
         r'^add/$',
         permission_required('dsc.add_deviceserver')(DeviceServerAddView.as_view()),
         name='deviceserver_add'),

    url(
         r'^search/$',
         search_view,
         name='deviceserver_search'),

    url(
         r'^autocomplete/manufacturers/$',
         DeviceServerManufacturerAutocomplete.as_view(),
         name='deviceserver_manufacturers'),

    url(
         r'^autocomplete/products/$',
         DeviceServerProductAutocomplete.as_view(),
         name='deviceserver_products'),

    url(
         r'^autocomplete/families/$',
         DeviceServerFamilyAutocomplete.as_view(),
         name='deviceserver_families'),

    url(
         r'^autocomplete/buses/$',
         DeviceServerBusAutocomplete.as_view(),
         name='deviceserver_buses'),

    url(
         r'^autocomplete/licenses/$',
         DeviceServerLicenseAutocomplete.as_view(),
         name='deviceserver_licenses'),

)

