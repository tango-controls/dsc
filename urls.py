from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'dsc/^$', views.index, name='index'),
]