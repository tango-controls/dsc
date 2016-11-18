# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, RequestContext
from django.views.generic import TemplateView, FormView
from django.db import transaction
from webu.custom_models.views import CustomModelDetailView
from webu.views import CMSDetailView
from tango.views import BreadcrumbMixinDetailView

from django_tables2 import RequestConfig

import dal.autocomplete

from xmi_parser import TangoXmiParser
from tables import DeviceAttributesTable, DeviceCommandsTable, DevicePipesTable, \
    DevicePropertiesTable, DeviceServerSearchTable
from forms import DeviceServerAddForm, DeviceServerSearchForm
import models as dsc_models





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


def search_view(request):
    """Search is done with function """
    context = RequestContext(request)
    table = None
    if request.method == 'GET':
        form = DeviceServerSearchForm(request.GET)
        if form.is_valid():
            # Do something with the data
            man = form.cleaned_data.get('manufacturer', None)
            prod = form.cleaned_data.get('product', None)
            family = form.cleaned_data.get('family', None)
            bus = form.cleaned_data.get('bus', None)

            q = dsc_models.DeviceClassInfo.objects

            if man:
                q = q.filter(manufacturer__icontains=man)

            if prod:
                q = q.filter(product_reference__icontains=prod)

            if family:
                q = q.filter(class_family__icontains=family)

            if bus:
                q = q.filter(bus__icontains=bus)

            device_servers = []
            for cli in q.all():
                if cli.device_class.device_server not in device_servers:
                    device_servers.append(cli.device_class.device_server)

            table = DeviceServerSearchTable(device_servers)
            RequestConfig(request).configure(table)
    else:
        form = DeviceServerSearchForm()

    return render_to_response('dsc/deviceserver_search.html', {'form': form, 'table':table}, context)


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


class DeviceServerBusAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for bus fields"""
    def get_list(self):
        return dsc_models.DeviceClassInfo.objects.all().values_list('bus', flat=True).distinct()

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

            # make sure that database is consisten
            with transaction.atomic():
                # remember data passed from the form
                add_device = form.save()
                assert (isinstance(add_device, dsc_models.DeviceServerAddModel))
                add_device.created_by = self.request.user
                add_device.save()

                # mark  activity
                activity = dsc_models.DeviceServerActivity(activity_type=dsc_models.DS_ACTIVITY_ADD,
                                                           activity_info='The device server has been added to catalogue.',
                                                           created_by=self.request.user
                                                           )
                activity.save()

                self.device_server, old_ds = dsc_models.create_or_update(add_device,activity)
                self.device_server.save()

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
