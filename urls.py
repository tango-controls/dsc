from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^dsc/$', views.index, name='dsc_index'),
    url(r'^dsc/ds/(?P<device_server_id>.*)$', views.device_server_detail, name='device_server__detail')
]
