from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import *

# Create your views here


def index(request):
    '''
    Renders index page
    :param request: HTTP request provided by the Django
    :return: return to be
    '''
    return HttpResponse("Hello, world. You're at the DS Catalogue index.")

def device_server_detail(request,device_server_id):
    device_server = get_object_or_404(DeviceServer,pk=device_server_id)
    context = {
        'device_server':device_server,
    }
    return render(request,'dsc/device_server_detail.html', context)
