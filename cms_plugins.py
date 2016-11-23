# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from webu.cms_plugins import LastPublishedObjectPluginBase

from cms.plugin_base import CMSPluginBase

from dsc.models import DeviceServerPluginModel, DeviceServer, DeviceServerActivity, DeviceServersActivityPluginModel

from dsc.tables import DeviceServerTable

from django_tables2 import RequestConfig

from django.template import RequestContext

import random

class DeviceServerPlugin(CMSPluginBase): #LastPublishedObjectPluginBase
    # TODO device server plugin filters etc
    model = DeviceServerPluginModel
    name = 'Device Servers Catalogue'
    render_template = "dsc/deviceserver_list.html"

    def get_instance_queryset(self, instance, request):
        queryset = super(DeviceServerPlugin, self).get_instance_queryset(instance, request)
        return queryset     #.order_by('name')

    def render(self, context, instance, placeholder):
        context = super(DeviceServerPlugin, self).render(context, instance, placeholder)
        context['table_class'] = DeviceServerTable
        # getting random 10 device servers
        q = DeviceServer.objects.filter(invalidate_activity=None)
        count = q.count()
        ds_list = []
        while len(ds_list)<10 and len(ds_list)<count:
            ds = random.choice(q)
            if ds not in ds_list:
                ds_list.append(ds)

        table = DeviceServerTable(ds_list)
        RequestConfig(context['request']).configure(table)
        context['table']= table
        #context['table_pagination'] = {
        #    'per_page': 20
        #}

        # clean context from nested context to get around of bug in context.flatten (django tracker #24765)

        context_inside = True
        # print type(context.dicts)

        while context_inside:
            # print '*******************************'
            new_context_dicts = []
            context_inside = False
            for d in context.dicts:
                # print type(d)
                # print '-----------------------------------'
                # print d
                if isinstance(d, RequestContext):
                    new_context_dicts.extend(d.dicts)
                    context_inside = True
                else:
                    new_context_dicts.append(d)
            context.dicts = new_context_dicts


        return context

plugin_pool.register_plugin(DeviceServerPlugin)


class DeviceServersActivityPlugin(CMSPluginBase): #LastPublishedObjectPluginBase
    # TODO device server plugin filters etc
    model = DeviceServersActivityPluginModel
    name = 'Device Servers Catalogue Activity'
    render_template = "dsc/inc/catalogue_activities.html"

    def get_instance_queryset(self, instance, request):
        queryset = super(DeviceServersActivityPlugin, self).get_instance_queryset(instance, request)
        return queryset     #.order_by('name')

    def render(self, context, instance, placeholder):
        context = super(DeviceServersActivityPlugin, self).render(context, instance, placeholder)

        # getting random 10 device servers
        q = DeviceServerActivity.objects.order_by('-created_at')
        count = DeviceServer.objects.all().count()
        ds_list = []
        activities = []
        i=0
        while len(ds_list)<instance.items_number and len(ds_list) < count and i < len(q):
            activity = q[i]
            if activity.device_server not in ds_list:
                ds_list.append(activity.device_server)
                activities.append(activity)
            i += 1

        context['activities']= activities


        context_inside = True
        # print type(context.dicts)

        while context_inside:
            # print '*******************************'
            new_context_dicts = []
            context_inside = False
            for d in context.dicts:
                # print type(d)
                # print '-----------------------------------'
                # print d
                if isinstance(d, RequestContext):
                    new_context_dicts.extend(d.dicts)
                    context_inside = True
                else:
                    new_context_dicts.append(d)
            context.dicts = new_context_dicts


        return context

plugin_pool.register_plugin(DeviceServersActivityPlugin)
