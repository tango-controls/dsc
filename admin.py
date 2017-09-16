from django.contrib import admin
from .models import *
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from webu.admin import (
    FrontendEditableAdminMixinFactory,
    WebuTopModelAdminMixin, WebuBottomModelAdminMixin,
)


# Register your models here.
@admin.register(DeviceServer, DeviceClass, DeviceServerRepository,
                DeviceServerDocumentation, DeviceClassInfo,
                DeviceServerActivity, DeviceServerLicense,
                DeviceAttribute, DeviceCommand,
                DevicePipe, DeviceProperty, DeviceAttributeInfo, DeviceServerAddModel, DeviceServerUpdateModel,
                DeviceClassFamily)
class DeviceServersAdminPanel(admin.ModelAdmin):
    pass




