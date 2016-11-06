# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import models as dsc_models
from forms import DeviceServerAddForm
from tables import DeviceServerTable
from django.views.generic import TemplateView, FormView
from webu.custom_models.views import CustomModelDetailView
from webu.views import CMSListView, CMSDetailView
from tango.views import ContentActionViewMixin, FilterGetFormViewMixin, BreadcrumbMixinDetailView
from django_tables2 import SingleTableView
from tables import DeviceAttributesTable, DeviceCommandsTable, DevicePipesTable, DevicePropertiesTable
from xmi_parser import TangoXmiParser
from django.core.urlresolvers import reverse, reverse_lazy
#import django_filters

from django.shortcuts import render
from django_tables2 import RequestConfig

# Create your views here

###################################################################################################
# DS Catalogue main view - Device Servers list
class DeviceServerDetailView(BreadcrumbMixinDetailView, CustomModelDetailView, CMSDetailView):
    """View that displays details of device server."""
    model = dsc_models.DeviceServer
    template_name = 'dsc/deviceserver_detail.html'

    def get_context_data(self, **kwargs):
        """Default context data have to be supplemented with related models objects."""
        context = super(DeviceServerDetailView, self).get_context_data(**kwargs)

        # get all classes
        context['device_classes'] = context['deviceserver'].device_classes.all()
        # for all classes tables of attributes, properties  and so will be provided
        context['specifications'] = {}

        for cl in context['device_classes']:
            context['specifications'][cl.name] = {}
            context['specifications'][cl.name]['properties_table'] = DevicePropertiesTable(cl.properties.all())
            context['specifications'][cl.name]['attributes_table'] = DeviceAttributesTable(cl.attributes.all())
            context['specifications'][cl.name]['commands_table'] = DeviceCommandsTable(cl.commands.all())
            context['specifications'][cl.name]['pipes_table'] = DevicePipesTable(cl.pipes.all())
            context['specifications'][cl.name]['info'] = cl.info
            context['specifications'][cl.name]['cl'] = cl

        return context


class DeviceServerAddView(FormView):
    """ View that process device server adding to the system. """

    template_name = 'dsc/deviceserver_add.html'
    form_class = DeviceServerAddForm
    device_server = None


    def form_valid(self, form):
        """This method is called when form has been filed correctly. It creates model objects and save them."""

        # just let IDE knows the type
        assert (isinstance(form, DeviceServerAddForm))

        # remember data passed from the form
        add_device = form.save()
        assert (isinstance(add_device,dsc_models.DeviceServerAddModel))

        if form.cleaned_data['use_uploaded_xmi_file']:
            # use xmi file
            parser = TangoXmiParser(xml_string=form.cleaned_data['xmi_string'])
            print "\n----------------\n\nproperly paresed XMI file :)\n\n-----\n"

            # device server object
            device_server = parser.get_device_server()
            device_server.add_device_object = add_device
            device_server.license.save()

            # if manual info provided override defaults
            if form.cleaned_data['use_manual_info']:
                if len(form.cleaned_data['name'])>0:
                    device_server.name = form.cleaned_data['name']

                if len(form.cleaned_data['description'])>0:
                    device_server.description = form.cleaned_data['description']

            device_server.save()

            # classes
            cls = parser.get_device_classes()
            for cl in cls:
                # save class
                assert (isinstance(cl,dsc_models.DeviceClass))
                cl.device_server = device_server
                cl.save()

                # create and save class info object
                class_info = parser.get_device_class_info(cl)
                assert (isinstance(class_info, dsc_models.DeviceClassInfo))
                class_info.device_class = cl

                # if manual info provided override defaults
                if form.cleaned_data['use_manual_info']:
                    if len(form.cleaned_data['contact_email'])>0:
                        class_info.contact_email = form.cleaned_data['contact_email']



                class_info.save()

                # create and save attributes
                attributes = parser.get_device_attributes(cl)
                for attrib in attributes:
                    assert(isinstance(attrib,dsc_models.DeviceAttribute))
                    attrib.device_class = cl
                    attrib.save()

                # create and save commands
                commands = parser.get_device_commands(cl)
                for command in commands:
                    assert (isinstance(command, dsc_models.DeviceCommand))
                    command.device_class = cl
                    command.save()

                # create and save pipes
                pipes = parser.get_device_pipes(cl)
                for pipe in pipes:
                    assert (isinstance(pipe, dsc_models.DevicePipe))
                    pipe.device_class = cl
                    pipe.save()

                # create and save properties
                properties = parser.get_device_properties(cl)
                for prop in properties:
                    assert (isinstance(prop, dsc_models.DeviceProperty))
                    prop.device_class = cl
                    prop.save()
        else:
            # use manually provided info
            pass

        # process documentation
        if form.cleaned_data['upload_readme']:
            device_server.readme=add_device.readme_file

        if form.cleaned_data['other_documentation1'] and len(form.cleaned_data['documentation1_url'])>0 \
            and len(form.cleaned_data['documentation1_type'])>0:
            doc = dsc_models.DeviceServerDocumentation(documentation_type=form.cleaned_data['documentation1_type'],
                                                       url = form.cleaned_data['documentation1_url'])
            doc.device_server = device_server
            doc.save()

        # process repository
        if form.cleaned_data['available_in_repository'] and len(form.cleaned_data['repository_type'])>0 \
            and len(form.cleaned_data['repository_url'])>0:
            repo = dsc_models.DeviceServerRepository(repository_type=form.cleaned_data['repository_type'],
                                                     url=form.cleaned_data['repository_url'],
                                                     path_in_repository=form.cleaned_data['repository_path']
                                                     )
            repo.device_server = device_server
            repo.save()

        # final save
        device_server.save()
        self.device_server = device_server

        return super(DeviceServerAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse('deviceserver_detail', kwargs={'pk': self.device_server.pk})
