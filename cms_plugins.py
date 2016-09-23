# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from webu.cms_plugins import LastPublishedObjectPluginBase

from cms.plugin_base import CMSPluginBase

from dsc.models import DeviceServerPluginModel, DeviceServer

from dsc.tables import DeviceServerTable

from django_tables2 import RequestConfig

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
        #context['table_class'] = DeviceServerTable
        table = DeviceServerTable(DeviceServer.objects.all())
        #RequestConfig(request).configure(table)
        context['table'] = table
        #context['table_pagination'] = {
        #    'per_page': 20
        #}
        return context

plugin_pool.register_plugin(DeviceServerPlugin)
