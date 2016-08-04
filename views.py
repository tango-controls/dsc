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

def ds_detail(request,device_server_id):
    device_server = get_object_or_404(DeviceServer,pk=device_server_id)
    return HttpResponse("Hello, world. Soon, you will see DS detail here.")
