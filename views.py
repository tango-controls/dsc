from django.shortcuts import render
from django.http import HttpResponse

# Create your views here


def index(request):
    '''
    Renders index page
    :param request: HTTP request provided by the Django
    :return: return to be
    '''
    return HttpResponse("Hello, world. You're at the DS Catalogue index.")

def ds_detail(request):
    return HttpResponse("Hello, world. Soon, you will see DS detail here.")