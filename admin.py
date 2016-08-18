from django.contrib import admin
from .models import *
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from webu.admin import (
    FrontendEditableAdminMixinFactory,
    WebuTopModelAdminMixin, WebuBottomModelAdminMixin,
)
# Register your models here.
#TODO Administracja wszystkimi obiektami DSC
'''
@admin.register(DeviceClass, DeviceServerRepository,
                DeviceServerDocumentation, DeviceClassInfo,
                DeviceServerActivity, DeviceServerLicense,
                DeviceAttribute, DeviceCommand,
                DevicePipe, DeviceProperty, DeviceAttributeInfo)
'''


class DeviceServersAdmin(WebuTopModelAdminMixin,
    FrontendEditableAdminMixinFactory('name'),
    PlaceholderAdminMixin,
    WebuBottomModelAdminMixin,
    admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by', 'license')
    list_filter = ('name', 'created_at', 'created_by', 'license')

    pass

admin.site.register(DeviceServer, DeviceServersAdmin)