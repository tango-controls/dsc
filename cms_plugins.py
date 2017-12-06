# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django_tables2 import RequestConfig
from django.template import RequestContext
import random

from dsc.models import DeviceServerPluginModel, DeviceServer, DeviceServerActivity, DeviceServersActivityPluginModel, \
    DeviceClassInfo, filtered_device_servers, search_device_servers, DeviceServerOldPluginModel, \
    DeviceServerSearchPluginModel

from dsc.tables import DeviceServerTable


class DeviceServerOldPlugin(CMSPluginBase): #LastPublishedObjectPluginBase

    model = DeviceServerOldPluginModel
    name = 'Device Classes Catalogue Old'
    render_template = "dsc/catalogue_frontpage_old.html"
    cache = False

    def render(self, context, instance, placeholder):

        # prepare list of families
        families = DeviceClassInfo.objects.filter(invalidate_activity=None).order_by('class_family').\
            values_list('class_family', flat=True).distinct()

        families_count = {}
        for f in families:
            if f=='':
                f = 'Other'
            families_count[f] = families_count.get(f,0)+DeviceServer.objects.filter(invalidate_activity=None).\
                filter(device_classes__info__class_family=f).distinct().count()

        context['families_count'] = sorted(families_count.iteritems())
        context['families'] = families

        context['count_all'] = DeviceServer.objects.filter(invalidate_activity=None).count()

        # table of device servers
        request = context['request']
        family = request.GET.get('family', None)
        search_text = request.GET.get('search', None)
        if search_text is not None:
            query = search_device_servers(search_text)
            context['search'] = search_text
        else:
            if family is not None:
                query =  DeviceServer.objects.filter(invalidate_activity=None).\
                    filter(device_classes__info__class_family=family)
            else:
                query = DeviceServer.objects.filter(invalidate_activity=None).\
                    order_by('-created_at')

        table = DeviceServerTable(query.distinct())
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
        context['device_servers'] = table
        context['family'] = family

        # clean context from nested context to get around of bug in context.flatten (django tracker #24765)
        context_inside = True

        while context_inside:

            new_context_dicts = []
            context_inside = False
            for d in context.dicts:

                if isinstance(d, RequestContext):
                    new_context_dicts.extend(d.dicts)
                    context_inside = True
                else:
                    new_context_dicts.append(d)
            context.dicts = new_context_dicts


        return context

plugin_pool.register_plugin(DeviceServerOldPlugin)


class DeviceServerPlugin(CMSPluginBase): #LastPublishedObjectPluginBase

    model = DeviceServerPluginModel
    name = 'Device Classes Catalogue'
    render_template = "dsc/catalogue_frontpage.html"
    cache = False

    def render(self, context, instance, placeholder):

        # prepare list of families
        families = DeviceClassInfo.objects.filter(invalidate_activity=None).order_by('class_family').\
            values_list('class_family', flat=True).distinct()

        families_count = {}
        for f in families:
            if f=='':
                f = 'Other'
            families_count[f] = families_count.get(f,0)+DeviceServer.objects.filter(invalidate_activity=None).\
                filter(device_classes__info__class_family=f).distinct().count()

        context['families_count'] = sorted(families_count.iteritems())
        context['families'] = families

        context['count_all'] = DeviceServer.objects.filter(invalidate_activity=None).count()

        # table of device servers
        request = context['request']
        family = request.GET.get('family', None)
        search_text = request.GET.get('search', None)
        if search_text is not None:
            query = search_device_servers(search_text)
            context['search'] = search_text
        else:
            if family is not None:
                query =  DeviceServer.objects.filter(invalidate_activity=None).\
                    filter(device_classes__info__class_family=family)
            else:
                query = DeviceServer.objects.filter(invalidate_activity=None).\
                    order_by('-created_at')

        table = DeviceServerTable(query.distinct())
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
        context['device_servers'] = table
        context['family'] = family

        # clean context from nested context to get around of bug in context.flatten (django tracker #24765)
        context_inside = True

        while context_inside:

            new_context_dicts = []
            context_inside = False
            for d in context.dicts:

                if isinstance(d, RequestContext):
                    new_context_dicts.extend(d.dicts)
                    context_inside = True
                else:
                    new_context_dicts.append(d)
            context.dicts = new_context_dicts


        return context

plugin_pool.register_plugin(DeviceServerPlugin)


class DeviceServerSearchPlugin(CMSPluginBase): #LastPublishedObjectPluginBase

    model = DeviceServerSearchPluginModel
    name = 'Device Classes Catalogue Search'
    render_template = "dsc/inc/deviceserver_fulltextsearch.html"
    cache = False

    def render(self, context, instance, placeholder):

        # prepare list of families
        families = DeviceClassInfo.objects.filter(invalidate_activity=None).order_by('class_family').\
            values_list('class_family', flat=True).distinct()

        families_count = {}
        for f in families:
            if f=='':
                f = 'Other'
            families_count[f] = families_count.get(f,0)+DeviceServer.objects.filter(invalidate_activity=None).\
                filter(device_classes__info__class_family=f).distinct().count()

        context['families_count'] = sorted(families_count.iteritems())
        context['families'] = families

        context['count_all'] = DeviceServer.objects.filter(invalidate_activity=None).count()

        # table of device servers
        request = context['request']
        family = request.GET.get('family', None)
        search_text = request.GET.get('search', None)
        if search_text is not None:
            query = search_device_servers(search_text)
            context['search'] = search_text
        else:
            if family is not None:
                query =  DeviceServer.objects.filter(invalidate_activity=None).\
                    filter(device_classes__info__class_family=family)
            else:
                query = DeviceServer.objects.filter(invalidate_activity=None).\
                    order_by('-created_at')

        table = DeviceServerTable(query.distinct())
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
        context['device_servers'] = table
        context['family'] = family

        # clean context from nested context to get around of bug in context.flatten (django tracker #24765)
        context_inside = True

        while context_inside:

            new_context_dicts = []
            context_inside = False
            for d in context.dicts:

                if isinstance(d, RequestContext):
                    new_context_dicts.extend(d.dicts)
                    context_inside = True
                else:
                    new_context_dicts.append(d)
            context.dicts = new_context_dicts


        return context

plugin_pool.register_plugin(DeviceServerSearchPlugin)


class DeviceServersListPlugin(CMSPluginBase):
    """ Presents table with randomly picked-up device servers"""
    name = 'Device Classes list'
    render_template = "dsc/inc/deviceserver_list.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(DeviceServersListPlugin, self).render(context, instance, placeholder)
        context['table_class'] = DeviceServerTable
        request = context['request']

        man = request.GET.get('manufacturer', None)
        prod = request.GET.get('product', None)
        family = request.GET.get('family', None)
        bus = request.GET.get('bus', None)

        q = filtered_device_servers(manufacturer=man, product=prod, family=family, bus=bus)

        table = DeviceServerTable(q)
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
        context['device_servers'] = table

        # clean context from nested context to get around of bug in context.flatten (django tracker #24765)
        context_inside = True

        while context_inside:
            new_context_dicts = []
            context_inside = False
            for d in context.dicts:

                if isinstance(d, RequestContext):
                    new_context_dicts.extend(d.dicts)
                    context_inside = True
                else:
                    new_context_dicts.append(d)
            context.dicts = new_context_dicts

        return context


plugin_pool.register_plugin(DeviceServersListPlugin)


class DeviceServersRandomListPlugin(CMSPluginBase):
    """ Presents table with randomly picked-up device servers"""
    name = 'Device Classes random list'
    render_template = "dsc/inc/deviceserver_randomlist.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(DeviceServersRandomListPlugin, self).render(context, instance, placeholder)
        context['table_class'] = DeviceServerTable
        # getting random 10 device servers
        q = DeviceServer.objects.filter(invalidate_activity=None)
        count = q.count()
        ds_list = []
        while len(ds_list) < 10 and len(ds_list) < count:
            ds = random.choice(q)
            if ds not in ds_list:
                ds_list.append(ds)

        table = DeviceServerTable(ds_list)
        RequestConfig(context['request'], paginate={'per_page': 10}).configure(table)
        context['device_servers'] = table

        # clean context from nested context to get around of bug in context.flatten (django tracker #24765)
        context_inside = True

        while context_inside:
            new_context_dicts = []
            context_inside = False
            for d in context.dicts:

                if isinstance(d, RequestContext):
                    new_context_dicts.extend(d.dicts)
                    context_inside = True
                else:
                    new_context_dicts.append(d)
            context.dicts = new_context_dicts

        return context


plugin_pool.register_plugin(DeviceServersRandomListPlugin)

class DeviceServersActivityPlugin(CMSPluginBase): #LastPublishedObjectPluginBase
    # TODO device server plugin filters etc
    model = DeviceServersActivityPluginModel
    name = 'Device Classes Catalogue Activity'
    render_template = "dsc/inc/catalogue_activities.html"
    cache = False

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
