# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import models as dsc_models
from forms import DeviceServerAddForm, DeviceServerSearchForm
from tables import DeviceServerTable
from django.views.generic import TemplateView, FormView
from webu.custom_models.views import CustomModelDetailView
from webu.views import CMSListView, CMSDetailView
from tango.views import ContentActionViewMixin, FilterGetFormViewMixin, BreadcrumbMixinDetailView
from django_tables2 import SingleTableView
from tables import DeviceAttributesTable, DeviceCommandsTable, DevicePipesTable, DevicePropertiesTable
from xmi_parser import TangoXmiParser
from django.core.urlresolvers import reverse
from django.db import models
import dal.autocomplete
#import django_filters

from django.shortcuts import render
from django_tables2 import RequestConfig

# Create your views here


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

        readme_file = context['deviceserver'].readme
        try:
            context['readme'] = readme_file.read()
        except:
            pass
        return context


class DeviceServerSearchView(FormView):
    """View that process search """
    template_name = 'dsc/deviceserver_search.html'
    form_class = DeviceServerSearchForm

    def form_valid(self, form):
        return super(DeviceServerSearchView, self).form_valid(form)

    def get_success_url(self):
        return reverse('deviceserver_detail', kwargs={'pk': self.device_server.pk})


class DeviceServerManufacturerAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for manufacturer fields"""
    def get_list(self):
        return dsc_models.DeviceClassInfo.objects.all().values_list('manufacturer',flat=True).distinct()


class DeviceServerProductAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for product fields"""
    def get_list(self):

        manufacturer = self.forwarded.get('manufacturer', None)
        if manufacturer:
            return dsc_models.DeviceClassInfo.objects.filter(manufacturer=manufacturer).\
                values_list('product_reference',flat=True).distinct()

        return dsc_models.DeviceClassInfo.objects.\
            values_list('product_reference', flat=True).distinct()


class DeviceServerFamilyAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for product fields"""
    def get_list(self):
        return dsc_models.DeviceClassInfo.objects.all().values_list('class_family', flat=True).distinct()


class DeviceServerLicenseAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for product fields"""
    def get_list(self):
        return dsc_models.DeviceServerLicense.objects.all().values_list('name', flat=True).distinct()


class DeviceServerAddView(FormView):
    """ View that process device server adding to the system. """

    template_name = 'dsc/deviceserver_add.html'
    form_class = DeviceServerAddForm
    device_server = None


    def form_valid(self, form):
        """This method is called when form has been filed correctly. It creates model objects and save them."""
        try:
            # just let IDE knows the type
            assert (isinstance(form, DeviceServerAddForm))

            # remember data passed from the form
            add_device = form.save()
            assert (isinstance(add_device,dsc_models.DeviceServerAddModel))
            add_device.created_by = self.request.user
            add_device.save()

            if form.cleaned_data['use_uploaded_xmi_file']:
                # use xmi file
                parser = TangoXmiParser(xml_string=form.cleaned_data['xmi_string'])
                print "\n----------------\n\nproperly paresed XMI file :)\n\n-----\n"

                # device server object
                device_server = parser.get_device_server()
                device_server.add_device_object = add_device
                device_server.license.save()

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
                device_server = dsc_models.DeviceServer(name='', description='')
                device_server.add_device_object = add_device

            # if manual info provided override defaults
            if form.cleaned_data['use_manual_info']:
                if len(form.cleaned_data['name']) > 0:
                    device_server.name = form.cleaned_data['name']

                if len(form.cleaned_data['description']) > 0:
                    device_server.description = form.cleaned_data['description']

                if len(form.cleaned_data['license_name'])>0:
                    try:
                        lic = dsc_models.DeviceServerLicense.objects.get(name=form.cleaned_data['license_name'])
                    except dsc_models.DeviceServerLicense.DoesNotExist:
                        lic = dsc_models.DeviceServerLicense(name=form.cleaned_data['license_name'])
                        lic.save()

                    device_server.license = lic
                device_server.save()

                cl = dsc_models.DeviceClass(name=form.cleaned_data['name'],
                                            description=form.cleaned_data['description'],
                                            class_copyright=form.cleaned_data['class_copyright'],
                                            language=form.cleaned_data['language'],
                                            device_server=device_server
                                            )
                if lic is not None:
                    cl.license = lic

                cl.save()

                cl_info = dsc_models.DeviceClassInfo(device_class=cl,
                                                     contact_email=form.cleaned_data['contact_email'],
                                                     class_family=form.cleaned_data.get('class_family','Not defined'),
                                                     platform=form.cleaned_data['platform'],
                                                     bus=form.cleaned_data['bus'],
                                                     manufacturer=form.cleaned_data['manufacturer'],
                                                     product_reference=form.cleaned_data['product_reference'],
                                                     key_words=form.cleaned_data['key_words']
                                                     )
                cl_info.save()




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
            device_server.created_by=self.request.user
            device_server.save()
            self.device_server = device_server

            # mark  activity
            activity = dsc_models.DeviceServerActivity(activity_type=dsc_models.DS_ACTIVITY_ADD,
                                                       activity_info='The device server has been added to catalogue.',
                                                       device_server=device_server,
                                                       created_by=self.request.user
                                                       )
            activity.save()

            # mark success
            add_device.processed_ok = True
            add_device.save()
        except Exception as e:
            add_device.processed_with_errors = True
            add_device.save()
            raise e

        return super(DeviceServerAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse('deviceserver_detail', kwargs={'pk': self.device_server.pk})
