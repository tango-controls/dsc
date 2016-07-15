from django.db import models
from django.conf import settings

# Create your models here.

AUTH_USER_MODEL = settings.AUTH_USER_MODEL


class DeviceServer(models.Model):
    """Model for a DeviceServer basic entities."""
    # TODO: implement interface

    name = models.CharField()

    description = models.TextField()

    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        editable=False,
        on_delete=models.SET_NULL, # important to avoid deletion of entries when user is removed from the system
        related_name='created_device_servers',
        blank=True, null=True,)

    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True)

    license = models.ForeignKey(
        DeviceServerLicnese,
        editable=True,
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when user is removed from the system
        related_name='licensed_device_servers',
        blank=True, null=True,)


class DeviceServerActivity(models.Model):
    """Model for tracking of activity around Device Server."""
    activity_type = models.CharField()  # TODO: implement activity types choices

    activity_info = models.TextField()

    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        editable=False,
        on_delete=models.SET_NULL, # important to avoid deletion of entries when user is removed from the system
        related_name='created_device_servers',
        blank=True, null=True,)

    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True)

    device_server = models.ForeignKey(DeviceServer, related_name='activities')


class DeviceServerDocumentation(models.Model):
    """Model for providing reference to device server documentation."""
    documentation_type = models.SludgeField()  # TODO: implement documentation type choices
    url = models.URLField()
    device_server = models.ForeignKey(DeviceServer, related_name='documentation')


class DeviceServerRepository(models.Model):
    """Model for referencing repository where the device serve could be found"""
    repository_type = models.SludgeField()  # TODO: implement repository types choices
    url = models.URLField()
    path_in_repository = models.CharField()
    device_server = models.OneToOne(DeviceServer, related_name='repository')


class DeviceServerLicnese(models.Model):
    """Model for providing info about licencing of devcie servers."""
    name = models.CharField(primary_key=True)
    description = models.TextField()
    url = models.URLField(blank=True)


class DeviceClass(models.Model):
    """Model to describe device classes implemented by device server"""
    name =models.CharField(max_length=64)
    description = models.TextField()
    device_server = models.ForeignKey(DeviceServer,related_name='device_classes')


class DeviceClassInfo(models.Model):
    """Model for information about device server."""
    device_class = models.OneToOne(DeviceClass, related_name='info')
    xmi_file = models.CharField(max_length=128) # this will store a link to source xmi_file
    contact_email = models.EmailField()
    class_family = models.CharField()  # TODO: implement class family choices
    platform = models.CharField()  # TODO: implement platform choices
    bus = models.CharField()  # at the beginning there will not be a manufacturer table, TODO: implement bus choices
    manufacturer = models.CharField()  # at the beginning there will not be a manufacturer table
    key_words = models.SludgeField()


class DeviceAttribute(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField()
    description = models.TextField()
    attribute_type = models.CharField()  # TODO: implement choice of attr type
    data_type = models.CharField()  # TODO: implement choice of attr data type
    device_class = models.ForeignKey(DeviceClass, related_name='attributes')


class DeviceCommand(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField()
    description = models.TextField()
    input_type = models.CharField()  # TODO: implement choice of cmd input type
    output_type = models.CharField()  # TODO: implement choice of cmd output type
    device_class = models.ForeignKey(DeviceClass, related_name='commands')


class DevicePipe(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField()
    description = models.TextField()
    device_class = models.ForeignKey(DeviceClass, related_name='pipes')


class DeviceProperty(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField()
    description = models.TextField()
    property_type = models.CharField()  # TODO: implement choice of property type
    device_class = models.ForeignKey(DeviceClass, related_name='properties')


class DeviceAttributeInfo(models.Model):
    """Model for providing additional infos about attributes. For future extenstion."""
    device_attribute = models.OneToOne(DeviceAttribute,related_name='attribute_info')
    # TODO: implement extended interface of DeviceAttributeInfo
