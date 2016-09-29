from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dsc/', include('dsc.urls_dsc')),
    url(r'', include('cms.urls')),
]