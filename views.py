# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import DeviceServer
from forms import DeviceServerAddForm
from tables import DeviceServerTable
from django.views.generic import TemplateView, FormView
from webu.custom_models.views import CustomModelDetailView
from webu.views import CMSListView, CMSDetailView
from tango.views import ContentActionViewMixin, FilterGetFormViewMixin, BreadcrumbMixinDetailView
from django_tables2 import SingleTableView
from tables import DeviceAttributesTable, DeviceCommandsTable, DevicePipesTable, DevicePropertiesTable
from xmi_parser import TangoXmiParser
#import django_filters

from django.shortcuts import render
from django_tables2 import RequestConfig

# Create your views here

###################################################################################################
# DS Catalogue main view - Device Servers list

class DeviceServerDetailView(BreadcrumbMixinDetailView, CustomModelDetailView, CMSDetailView):
    model = DeviceServer
    template_name = 'dsc/deviceserver_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DeviceServerDetailView, self).get_context_data(**kwargs)

        # get all classes
        context['device_classes'] = context['deviceserver'].device_classes.all()
        # for all classes tables of attributes, properties  and so will be provided
        context['specifications'] = {}

        context['abc'] = {'bca':'xyz'}

        for cl in context['device_classes']:
            context['specifications'][cl.name] = {}
            context['specifications'][cl.name]['properties_table'] = DevicePropertiesTable(cl.properties.all())
            context['specifications'][cl.name]['attributes_table'] = DeviceAttributesTable(cl.attributes.all())
            context['specifications'][cl.name]['commands_table'] = DeviceCommandsTable(cl.commands.all())
            context['specifications'][cl.name]['pipes_table'] = DevicePipesTable(cl.pipes.all())
            context['specifications'][cl.name]['info'] = cl.info
            context['specifications'][cl.name]['cl'] = cl
        print '****************************'
        print context
        print '****************************'

        return context


class DeviceServerAddView(FormView):

    template_name = 'dsc/deviceserver_add.html'
    form_class = DeviceServerAddForm

    def form_valid(self, form):

        # just let IDE knows the type
        assert (isinstance(form, DeviceServerAddForm))

        # remember data passed from the form
        form.save()

        if form.cleaned_data['use_uploaded_xmi_file']:
            # use xmi file
            parser = TangoXmiParser(form.cleaned_data['xmi_file'])
            print ""
        else:
            # use manualy provided info
            pass

        return super(DeviceServerAddView, self).form_valid(form)
