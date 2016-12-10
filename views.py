# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, RequestContext
from django.views.generic import TemplateView, FormView, UpdateView
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from webu.custom_models.views import CustomModelDetailView
from webu.views import CMSDetailView
from tango.views import BreadcrumbMixinDetailView

from django_tables2 import RequestConfig

import dal.autocomplete

from xmi_parser import TangoXmiParser
from tables import DeviceAttributesTable, DeviceCommandsTable, DevicePipesTable, \
    DevicePropertiesTable, DeviceServerSearchTable
from forms import DeviceServerAddForm, DeviceServerSearchForm, DeviceServerUpdateForm
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
        context['device_classes'] = context['deviceserver'].device_classes.filter(invalidate_activity=None)
        # for all classes tables of attributes, properties  and so will be provided
        context['specifications'] = {}

        for cl in context['device_classes']:
            context['specifications'][cl.name] = {}
            context['specifications'][cl.name]['properties_table'] = \
                DevicePropertiesTable(cl.properties.filter(invalidate_activity=None))
            context['specifications'][cl.name]['attributes_table'] = \
                DeviceAttributesTable(cl.attributes.filter(invalidate_activity=None))
            context['specifications'][cl.name]['commands_table'] = \
                DeviceCommandsTable(cl.commands.filter(invalidate_activity=None))
            context['specifications'][cl.name]['pipes_table'] = \
                DevicePipesTable(cl.pipes.filter(invalidate_activity=None))
            context['specifications'][cl.name]['info'] = cl.info
            context['specifications'][cl.name]['cl'] = cl

        readme_file = context['deviceserver'].readme
        try:
            context['readme'] = readme_file.read()
        except:
            pass
        return context


class DeviceServerVerifyView(DeviceServerDetailView):

    def get_context_data(self, **kwargs):
        """Detail view context will provide device server which has to be updated with verified state"""
        context = super(DeviceServerVerifyView, self).get_context_data(**kwargs)
        device_server = context['deviceserver']
        assert isinstance(device_server, dsc_models.DeviceServer)
        if device_server.status==dsc_models.STATUS_NEW or device_server.status==dsc_models.STATUS_UPDATED:
            with transaction.atomic():
                verify_activity = dsc_models.DeviceServerActivity(
                    device_server=device_server,
                    activity_type=dsc_models.DS_ACTIVITY_VERIFICATION,
                    activity_info='Last update of the device server has been verified by %s.' %
                                  self.request.user.get_full_name(),
                    created_by=self.request.user
                )
                device_server.status=dsc_models.STATUS_VERIFIED
                verify_activity.save()
                device_server.save()
            context['message'] = 'This device server is verified.'
        else:
            if device_server.status!=dsc_models.STATUS_VERIFIED:
                context['message']='Only add or update operations can be verified.'
            if device_server.status==dsc_models.STATUS_VERIFIED:
                context['message']='This device server is already verified.'

        return context




def search_view(request):
    """Search is done with function """
    context = RequestContext(request)
    table_config = RequestConfig(request)
    table = None
    if request.method == 'GET':
        form = DeviceServerSearchForm(request.GET)
        if form.is_valid():
            # Do something with the data
            man = form.cleaned_data.get('manufacturer', None)
            prod = form.cleaned_data.get('product', None)
            family = form.cleaned_data.get('family', None)
            bus = form.cleaned_data.get('bus', None)
            key_words = form.cleaned_data.get('key_words', None)

            q = dsc_models.filtered_device_servers(manufacturer=man,
                                                   product=prod,
                                                   family=family,
                                                   bus=bus,
                                                   key_words=key_words)

            device_servers = q.distinct()

            table = DeviceServerSearchTable(device_servers)
        if table is not None:
            table_config.configure(table)

    form = DeviceServerSearchForm(initial=request.GET)

    return render_to_response('dsc/deviceserver_search.html', {'form': form, 'table': table}, context)


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


def update_class_description(request):
    pass

class DeviceServerUpdateView(BreadcrumbMixinDetailView, UpdateView):
    """ View that process device server adding to the system. """

    template_name = 'dsc/deviceserver_update.html'
    form_class = DeviceServerUpdateForm
    model = dsc_models.DeviceServer
    device_server = None

    def get_object(self):
        self.device_server = super(DeviceServerUpdateView, self).get_object()
        if self.device_server.created_by!=self.request.user \
            and not self.request.user.has_perm('dsc.admin_deviceserver'):
            self.template_name = 'dsc/deviceserver_notauthorized.html'
            return None
        update_object = dsc_models.DeviceServerUpdateModel().from_device_server(self.device_server)
        return update_object

    def get_context_data(self, **kwargs):
        context = super(DeviceServerUpdateView,self).get_context_data(**kwargs)
        if self.device_server.created_by!=self.request.user \
            and not self.request.user.has_perm('dsc.admin_deviceserver'):
            self.template_name = 'dsc/deviceserver_notauthorized.html'
            context['deviceserver'] = self.device_server
            context['operation'] = 'update'
        return context

    def form_valid(self, form):
        """This method is called when form has been filed correctly. It creates model objects and save them."""

        # just let IDE knows the type
        assert (isinstance(form, DeviceServerAddForm))

        # make sure that database is consisten
        with transaction.atomic():
            # remember data passed from the form
            update_object = form.save()
            assert (isinstance(update_object, dsc_models.DeviceServerAddModel))
            update_object.created_by = self.request.user
            update_object.save()

            # mark  activity
            activity = dsc_models.DeviceServerActivity(activity_type=dsc_models.DS_ACTIVITY_EDIT,
                                                       activity_info='The device server has been updated.',
                                                       created_by=self.request.user
                                                       )
            # it is related by other object, so it is good if it has primary key
            activity.save()

            # create device server
            self.device_server, old_ds = dsc_models.create_or_update(update_object, activity, self.device_server)
            #  just to make sure we save device server
            self.device_server.save()

            activity.device_server = self.device_server
            activity.device_server_backup = old_ds
            activity.save()

            # mark success
            update_object.activity = activity
            update_object.processed_ok = True
            update_object.save()

        return super(DeviceServerUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('deviceserver_detail', kwargs={'pk': self.device_server.pk})

@login_required
def deviceserver_delete_view(request, pk):
    context = RequestContext(request)
    device_server = dsc_models.DeviceServer.objects.get(pk=pk)
    if request.user != device_server.created_by and not request.user.has_perm('dsc.admin_deviceserver'):
        return render_to_response('dsc/deviceserver_notauthorized.html',
                                  {'operation': 'delete', 'deviceserver': device_server}, context)
    if request.method == 'GET':
        return render_to_response('dsc/deviceserver_delete_question.html',
                                      {'deviceserver': device_server}, context)
    else:
        with transaction.atomic():
            activity = dsc_models.DeviceServerActivity(activity_type=dsc_models.DS_ACTIVITY_DELETE,
                                                       activity_info='Device server %s has been deleted by %s %s.' % \
                                                                 (device_server.name,
                                                                  request.user.first_name,
                                                                  request.user.last_name),
                                                       device_server = device_server,
                                                       device_server_backup = device_server,
                                                       created_by = request.user)
            activity.save()
            device_server.invalidate_activity = activity
            device_server.status = dsc_models.STATUS_DELETED
            device_server.save()

        return render_to_response('dsc/deviceserver_delete_confirmed.html',
                                      {'deviceserver': device_server}, context)


def deviceserver_verify_view(request, pk):
    context = RequestContext(request)
    device_server = dsc_models.DeviceServer.objects.get(pk=pk)
    if request.user.has_perm('dsc.admin_deviceserver'):
        if device_server.status == dsc_models.STATUS_NEW or device_server.status == dsc_models.STATUS_UPDATED:
            with transaction.atomic():
                verify_activity = dsc_models.DeviceServerActivity(
                    device_server=device_server,
                    activity_type=dsc_models.DS_ACTIVITY_VERIFICATION,
                    activity_info='Last update of the device server has been verified by %s.' %
                                  request.user.get_full_name(),
                    created_by=request.user
                )
                device_server.status=dsc_models.STATUS_VERIFIED
                verify_activity.save()
                device_server.save()
            context['message'] = 'This device server is verified.'
        else:
            if device_server.status!=dsc_models.STATUS_VERIFIED:
                context['message']='Only add or update operations can be verified.'
            if device_server.status==dsc_models.STATUS_VERIFIED:
                context['message']='This device server is already verified.'

    return HttpResponseRedirect(reverse('deviceserver_detail', kwargs={'pk' : device_server.pk}))

class DeviceServerAddView(BreadcrumbMixinDetailView, FormView):
    """ View that process device server adding to the system. """

    template_name = 'dsc/deviceserver_add.html'
    form_class = DeviceServerAddForm
    device_server = None

    def get_object(self):
        return None

    def form_valid(self, form):
        """This method is called when form has been filed correctly. It creates model objects and save them."""

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
            # it is related by other object, so it is good if it has primary key
            activity.save()

            # create device server
            self.device_server, old_ds = dsc_models.create_or_update(add_device,activity)
            #  just to make sure we save device server
            self.device_server.save()

            activity.device_server = self.device_server
            activity.save()

            # mark success
            add_device.activity = activity
            add_device.processed_ok = True
            add_device.save()

        return super(DeviceServerAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse('deviceserver_detail', kwargs={'pk': self.device_server.pk})