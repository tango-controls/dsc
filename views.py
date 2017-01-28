# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, RequestContext
from django.views.generic import TemplateView, FormView, UpdateView
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from webu.custom_models.views import CustomModelDetailView
from webu.views import CMSDetailView
from tango.views import BreadcrumbMixinDetailView

from django_tables2 import RequestConfig

import dal.autocomplete

from xmi_parser import TangoXmiParser
from tables import DeviceAttributesTable, DeviceCommandsTable, DevicePipesTable, \
    DevicePropertiesTable, DeviceServerSearchTable, DeviceServerTable
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
        if context['deviceserver'].is_valid():
            context['device_classes'] = context['deviceserver'].device_classes.filter(invalidate_activity=None)
        else:
            activity = context['deviceserver'].invalidate_activity
            context['device_classes'] = context['deviceserver'].device_classes.all()
            context['device_classes'] = context['device_classes']| dsc_models.DeviceClass.objects. \
                                         filter(device_server__pk=activity.device_server.pk). \
                                         filter(invalidate_activity=None). \
                                         filter(create_activity__created_at__lt=activity.created_at). \
                                         filter(last_update_activity__created_at__lt=activity.created_at)

            context['device_classes'] = context['device_classes'] | dsc_models.DeviceClass.objects. \
                                         filter(invalidate_activity__device_server__pk=activity.device_server.pk). \
                                         filter(create_activity__created_at__lte=activity.created_at) . \
                                         filter(invalidate_activity__created_at__gte=activity.created_at)

            context['device_classes'] = context['device_classes'].distinct()

        # for all classes tables of attributes, properties  and so will be provided
        context['specifications'] = {}
        context['contacts'] = []
        for cl in context['device_classes']:
            assert isinstance(cl, dsc_models.DeviceClass)
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
            info = cl.info
            context['og_description'] = "This is a device server providing classes of "
            if info is not None:
                assert isinstance(info,dsc_models.DeviceClassInfo)
                if info.contact_email is not None and len(info.contact_email)>0 \
                        and info.contact_email not in context['contacts']:
                    context['contacts'].append(info.contact_email)
                if context['og_description'] == "This is a device server providing classes of ":
                    context['og_description'] += info.class_family
                else:
                    context['og_description'] += 'and '+ info.class_family
            context['og_description'] += " family."
        readme_file = context['deviceserver'].readme
        if hasattr(readme_file,'url'):
            readme_name, readme_ext = os.path.splitext(readme_file.name)
            readme_link = readme_file.url
            context['readme_link'] = readme_link
            context['readme_name'] = readme_file.name
            if readme_ext in ['', '.md', '.MD', '.txt', '.TXT', '.rst', '.RST']:
                try:
                    context['readme'] = readme_file.read()
                    if context['readme'].startswith('<html>'):
                        context['readme'] = False
                except:
                    pass
                return context

            if readme_ext in ['.rst', '.RST']:
                context['rst'] = True

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
                    activity_info='Last update to device class(es) have been verified by %s.' %
                                  self.request.user.get_full_name(),
                    created_by=self.request.user
                )
                device_server.status=dsc_models.STATUS_VERIFIED
                verify_activity.save()
                device_server.save()
            if device_server.device_classes.all().count()>1:
                context['message'] = 'Classes provided by device server are verified.'
            else:
                context['message'] = 'Class provided by this device server is verified.'
        else:
            if device_server.status!=dsc_models.STATUS_VERIFIED:
                context['message']='Only add or update operations can be verified.'
            if device_server.status==dsc_models.STATUS_VERIFIED:
                if device_server.device_classes.all().count() == 1:
                    context['message']='This device class is already verified.'
                else:
                    context['message'] = 'These device classes are already verified.'


        return context


def device_servers_list(request):
    ds_list = {}
    if request.method == 'GET':
        repository_url = request.GET.get('repository_url')
        repository_contact_email = request.GET.get('repository_contact_email')

    if request.method == 'POST':
        repository_url = request.POST.get('repository_url')
        repository_contact_email = request.POST.get('repository_contact_email')

    repositories = dsc_models.DeviceServerRepository.objects.filter(invalidate_activity=None)
    if repository_url is not None:
        repositories = repositories.filter(url=repository_url)

    if repository_contact_email is not None:
        repositories = repositories.filter(contact_email=repository_contact_email)

    for repo in repositories:
        ds = repo.device_server
        if ds is not None and not ds_list.has_key(ds.pk) and ds.is_valid():
            assert isinstance(ds,dsc_models.DeviceServer)
            if ds.last_update_activity is not None:
                last_update = ds.last_update_activity.created_at
            else:
                last_update = ds.created_at
            ds_list[ds.pk] = {
                'name': ds.name,
                'detail_url': request.build_absolute_uri(reverse('deviceserver_detail', kwargs={'pk': ds.pk})),
                'update_url': request.build_absolute_uri(reverse('deviceserver_update', kwargs={'pk': ds.pk})),
                'last_update': last_update,
                'last_update_method': ds.last_update_method(),
                'repository_url': str(repo.url),
                'repository_contact_email': str(repo.contact_email),
                'development_status': ds.development_status,
                'status': ds.status,
                'certified': str(ds.certified),
                'license': str(ds.license),
                'tag': repo.tag,
                'updated_by_script': ds.updated_by_script()
            }

            families = []
            manufacturers = []
            products = []
            buses = []
            cl_names = []
            for cl in ds.device_classes.filter(invalidate_activity=None):
                families.append(cl.info.class_family)
                manufacturers.append(cl.info.manufacturer)
                products.append(cl.info.product_reference)
                buses.append(cl.info.bus)
                cl_names.append(cl.name)

            ds_list[ds.pk]['families'] = families
            ds_list[ds.pk]['manufacturers'] = manufacturers
            ds_list[ds.pk]['products'] = products
            ds_list[ds.pk]['buses'] = buses
            ds_list[ds.pk]['class_names'] = cl_names
            docs = []
            for doc in ds.documentation(invalidate_activity=None):
                assert isinstance(doc, dsc_models.DeviceServerDocumentation)
                doc_dict = {
                    'title': str(doc.title),
                    'documentation_type': doc.documentation_type,
                    'url': doc.get_documentation_url(),
                    'updated_by_script': doc.updated_by_script(),
                    'pk': doc.pk
                }

                docs.append(doc_dict)
            ds_list[ds.pk]['documentation'] = docs

    return JsonResponse(ds_list)


def search_view(request):
    """Search is done with function """
    context = RequestContext(request)

    search_text = request.GET.get('search', '')
    family = request.GET.get('family', None)
    if search_text != '':
        query = dsc_models.search_device_servers(search_text)
        context['search'] = search_text
    else:
        query = dsc_models.DeviceServer.objects.filter(invalidate_activity=None)
        # dsc_models.filtered_device_servers(family=family)

    query = query.order_by('name')

    table = DeviceServerTable(query.distinct())
    RequestConfig(request, paginate={'per_page': 30}).configure(table)


    if 'breadcrumb_extra_ancestors' not in context:
        context['breadcrumb_extra_ancestors'] = []
    context['breadcrumb_extra_ancestors'].append((request.get_full_path(),'Search'))

    return render_to_response('dsc/deviceserver_search.html', {'device_servers': table,
                                                               'search': search_text,
                                                               }, context)


def advanced_search_view(request):
    """Search is done with function """
    context = RequestContext(request)
    table_config = RequestConfig(request, paginate={'per_page': 30})
    table = None
    man = ''
    prod = ''
    family = ''
    bus = ''
    key_words = ''
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

            device_servers = q.distinct().order_by('name')
            table = DeviceServerSearchTable(device_servers)

        if table is not None:
            table_config.configure(table)

    form = DeviceServerSearchForm(initial=request.GET)

    if 'breadcrumb_extra_ancestors' not in context:
        context['breadcrumb_extra_ancestors'] = []
    context['breadcrumb_extra_ancestors'].append((request.get_full_path(),'Search'))

    return render_to_response('dsc/deviceserver_advanced_search.html', {'form': form, 'table': table,
                                                               'manufacturer': man,
                                                               'product': prod,
                                                               'family': family,
                                                               'bus': bus,
                                                               'key_words': key_words
                                                               }, context)


def families_view(request):
    """Families is done with function """
    context = RequestContext(request)

    # prepare list of families
    families = dsc_models.DeviceClassInfo.objects.filter(invalidate_activity=None).order_by('class_family'). \
        values_list('class_family', flat=True).distinct()

    families_count = {}
    for f in families:
        if f == '':
            f = 'Other'
        families_count[f] = families_count.get(f, 0) + dsc_models.DeviceServer.objects.filter(invalidate_activity=None). \
            filter(device_classes__info__class_family=f).distinct().count()

    families_count = sorted(families_count.iteritems())

    count_all = dsc_models.DeviceServer.objects.filter(invalidate_activity=None).count()


    search_text = request.GET.get('search', '')
    family = request.GET.get('family', '')
    if family != '':
        query = dsc_models.filtered_device_servers(family=family)
    else:
        query = dsc_models.DeviceServer.objects.filter(invalidate_activity=None)

    query = query.order_by('name')

    table = DeviceServerTable(query.distinct())
    RequestConfig(request, paginate={'per_page': 30}).configure(table)

    if 'breadcrumb_extra_ancestors' not in context:
        context['breadcrumb_extra_ancestors'] = []
    context['breadcrumb_extra_ancestors'].append((request.get_full_path(),'Families'))

    return render_to_response('dsc/deviceserver_families.html', {'device_servers': table,
                                                                 'search': search_text,
                                                                 'family': family,
                                                                 'families': families,
                                                                 'families_count': families_count,
                                                                 'count_all': count_all
                                                                }, context)


class DeviceServerManufacturerAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for manufacturer fields"""
    def get_list(self):
        m = list(dsc_models.DeviceClassInfo.objects.all().order_by('manufacturer').values_list('manufacturer',flat=True).distinct())
        if self.request.GET.get('q',None) is not None:
            m.append(self.request.GET.get('q',None))

        return m


class DeviceServerProductAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for product fields"""
    def get_list(self):

        manufacturer = self.forwarded.get('manufacturer', None)
        if manufacturer:
            p=list(dsc_models.DeviceClassInfo.objects.filter(manufacturer=manufacturer). \
                   order_by('product_reference').values_list('product_reference',flat=True).distinct())
        else:
            p=list(dsc_models.DeviceClassInfo.objects. \
                   order_by('product_reference').values_list('product_reference', flat=True).distinct())

        if self.request.GET.get('q',None) is not None:
            p.append(self.request.GET.get('q',None))

        return p


class DeviceServerFamilyAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for product fields"""
    def get_list(self):
        f = list(dsc_models.DeviceClassInfo.objects.all().order_by('class_family').values_list('class_family', flat=True).distinct())

        return f


class DeviceServerBusAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for bus fields"""
    def get_list(self):
        b=list(dsc_models.DeviceClassInfo.objects.all().order_by('bus').values_list('bus', flat=True).distinct())
        if self.request.GET.get('q',None) is not None:
            b.append(self.request.GET.get('q',None))
        return b


class DeviceServerLicenseAutocomplete(dal.autocomplete.Select2ListView):
    """Provide autocomplete feature for product fields"""
    def get_list(self):
        k=list(dsc_models.DeviceServerLicense.objects.all().values_list('name', flat=True).distinct())
        if self.request.GET.get('q',None) is not None:
            k.append(self.request.GET.get('q',None))
        return k



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

        update_object = dsc_models.DeviceServerUpdateModel().from_device_server(self.device_server,
                                                            device_class=self.request.GET.get('device_class', None))
        update_object.use_manual_info = False
        update_object.use_uploaded_xmi_file = False
        update_object.use_url_xmi_file = False
        return update_object

    def get_context_data(self, **kwargs):
        context = super(DeviceServerUpdateView,self).get_context_data(**kwargs)
        if self.device_server.created_by!=self.request.user \
            and not self.request.user.has_perm('dsc.admin_deviceserver'):
            self.template_name = 'dsc/deviceserver_notauthorized.html'
            context['deviceserver'] = self.device_server
        context['deviceserver'] = self.device_server
        context['operation'] = 'update'
        device_class_pk = self.request.GET.get('device_class', None)
        if device_class_pk is not None:
            context['device_class'] = self.device_server.device_classes.filter(pk=device_class_pk).first()

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
            update_object.valid_xmi_string = form.cleaned_data.get('xmi_string', None)
            update_object.save()

            if update_object.add_class:
                ainfo = 'A device class has been added.'
            else:
                ainfo = 'The device class has been updated.'

            # mark  activity
            activity = dsc_models.DeviceServerActivity(activity_type=dsc_models.DS_ACTIVITY_EDIT,
                                                       activity_info=ainfo,
                                                       created_by=self.request.user
                                                       )
            # it is related by other object, so it is good if it has primary key
            activity.save()

            # create device server
            self.device_server, old_ds = dsc_models.create_or_update(update_object, activity, self.device_server,
                                                                device_class=self.request.GET.get('device_class', None))
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
    if 'breadcrumb_extra_ancestors' not in context:
        context['breadcrumb_extra_ancestors'] = []
    context['breadcrumb_extra_ancestors'].append((request.get_full_path(),'Advanced Search'))

    device_server = dsc_models.DeviceServer.objects.get(pk=pk)
    device_class = request.GET.get('device_class')
    if device_class is not None:
        clqf = device_server.device_classes.filter(pk=device_class)
        if clqf.count()==1:
            context['device_class']=clqf.first()

    if request.user != device_server.created_by and not request.user.has_perm('dsc.admin_deviceserver'):
        return render_to_response('dsc/deviceserver_notauthorized.html',
                                  {'operation': 'delete', 'deviceserver': device_server}, context)
    if request.method == 'GET':
        return render_to_response('dsc/deviceserver_delete_question.html',
                                      {'deviceserver': device_server}, context)
    else:
        with transaction.atomic():
            if device_class is None:
                clq = device_server.device_classes.all()
            else:
                clq = clqf
            if clq.count() == 1:
                if device_server.device_classes.all().count() == 1:
                    activity = dsc_models.DeviceServerActivity(activity_type=dsc_models.DS_ACTIVITY_DELETE,
                                                               activity_info='The device class %s has been deleted by %s %s.' % \
                                                                         (clq.first().name,
                                                                          request.user.first_name,
                                                                          request.user.last_name),
                                                               device_server = device_server,
                                                               device_server_backup = device_server,
                                                               created_by = request.user)
                    activity.save()
                    device_server.invalidate_activity = activity
                    device_server.status = dsc_models.STATUS_DELETED
                    device_server.save()
                elif device_server.device_classes.all().count() > 1:
                    activity = dsc_models.DeviceServerActivity(activity_type=dsc_models.DS_ACTIVITY_DELETE,
                                                               activity_info='The device class %s has been deleted by %s %s.' % \
                                                                             (clq.first().name,
                                                                              request.user.first_name,
                                                                              request.user.last_name),
                                                               device_server=device_server,
                                                               created_by=request.user)
                    activity.save()
                    backup_device_server = device_server.make_backup(activity=activity)
                    backup_device_server.save()
                    activity.device_server_backup = backup_device_server
                    activity.save()
                    cl = clq.first()
                    cl.device_server = backup_device_server
                    cl.invalidate_activity = activity
                    cl.save()
                else:
                    return render_to_response('dsc/deviceserver_delete_question.html',
                                              {'deviceserver': device_server}, context)


        return render_to_response('dsc/deviceserver_delete_confirmed.html',
                                      {'deviceserver': device_server}, context)


def deviceserver_verify_view(request, pk):
    context = RequestContext(request)
    if 'breadcrumb_extra_ancestors' not in context:
        context['breadcrumb_extra_ancestors'] = []
    context['breadcrumb_extra_ancestors'].append((request.get_full_path(),'Advanced Search'))
    device_server = dsc_models.DeviceServer.objects.get(pk=pk)
    if request.user.has_perm('dsc.admin_deviceserver'):
        if device_server.status == dsc_models.STATUS_NEW or device_server.status == dsc_models.STATUS_UPDATED:
            with transaction.atomic():
                verify_activity = dsc_models.DeviceServerActivity(
                    device_server=device_server,
                    activity_type=dsc_models.DS_ACTIVITY_VERIFICATION,
                    activity_info='Recent update of device classes in this device server has been verified by %s.' %
                                  request.user.get_full_name(),
                    created_by=request.user
                )
                device_server.status=dsc_models.STATUS_VERIFIED
                verify_activity.save()
                device_server.save()
            if device_server.device_classes.all().count()>1:
                context['message'] = 'Device classes are verified.'
            else:
                context['message'] = 'The device class is verified.'
        else:
            if device_server.status!=dsc_models.STATUS_VERIFIED:
                context['message']='Only add or update operations can be verified.'
            if device_server.status==dsc_models.STATUS_VERIFIED:
                context['message']='This device server and classes it provides are already verified.'

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
                                                       activity_info='The device class has been added to catalogue.',
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