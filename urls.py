from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^dsc/$', views.index, name='dsc_index'),
    url(r'^dsc/ds/(?P<device_server_id>.*)$', views.ds_detail, name='ds_view')
]
