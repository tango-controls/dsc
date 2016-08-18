# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import DeviceServer
from tables import DeviceServerTable
from django.views.generic import TemplateView
from webu.custom_models.views import CustomModelDetailView
from webu.views import CMSListView, CMSDetailView
from tango.views import ContentActionViewMixin, FilterGetFormViewMixin, BreadcrumbMixinDetailView
from django_tables2 import SingleTableView
#import django_filters

from django.shortcuts import render
from django_tables2 import RequestConfig

# Create your views here

# TEST PIOTRA, teraz DS detaled view class jest: DeviceServerDetailView
'''
def index(request):
    return HttpResponse("Hello, world. You're at the DS Catalogue index.")

def device_server_detail(request,device_server_id):
    device_server = get_object_or_404(DeviceServer,pk=device_server_id)
    context = {
        'device_server':device_server,
    }
    return render(request,'dsc/device_server_detail.html', context)
'''

###################################################################################################
# DS Catalogue main view - Device Servers list

class DeviceServerDetailView(BreadcrumbMixinDetailView, CustomModelDetailView, CMSDetailView):
    model = DeviceServer
    template_name = 'dsc/deviceserver_detail.html'

'''
class DeviceServerListView(FilterGetFormViewMixin, CMSListView):
    #TODO should be changed on table view
    paginate_by = 30
    paginate_orphans = 3
    model = DeviceServer
    filter_form_class = DeviceServerFilterForm
'''

#TODO opracować akcje niezbędne i zweryfikować to
class DeviceServerActionView(ContentActionViewMixin, DeviceServerDetailView):
    pass


class DeviceServerListView(SingleTableView):
        model = DeviceServer
        table_class = DeviceServerTable
        template_name = 'deviceserver_list.html'
        #table = DeviceServerTable(DeviceServer.objects.all())
        table_pagination = {
            'per_page': 20
        }

