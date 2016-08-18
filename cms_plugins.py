# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from webu.cms_plugins import LastPublishedObjectPluginBase

from cms.plugin_base import CMSPluginBase

from dsc.models import DeviceServerPluginModel

class DeviceServerPlugin (CMSPluginBase): #LastPublishedObjectPluginBase
    # TODO device server plugin filters etc
    model = DeviceServerPluginModel
    name = _('Device Server Catalogue')
    render_template = "dsc/deviceserver_list.html"
    def get_instance_queryset(self, instance, request):
        queryset = super(DeviceServerPlugin, self).get_instance_queryset(instance, request)
        return queryset     #.order_by('name')

plugin_pool.register_plugin(DeviceServerPlugin)
