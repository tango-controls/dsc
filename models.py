from django.db import models
from django.conf import settings

# Create your models here.

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

class DeviceServer(models.Model):
    """Model for a DeviceServer basic entities."""
    # TODO: implement interface

    name = models.CharField(max_length=64)

    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        editable=False,
        on_delete=models.SET_NULL,
        related_name='created_%(class)ss',
        blank=True, null=True,)

    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True)

    pass


class DeviceServerInfo(models.Model):
    """Model for information about device server."""
    # TODO: implement interface
    pass


class DeviceServerActivity(models.Model):
    """Model for tracking of activity around Device Server."""
    # TODO: implement interface
    pass


class DeviceServerDocumentation(models.Model):
    """Model for providing reference to device server documentation."""
    # TODO: implement interface
    pass


class DeviceServerRepository(models.Model):
    """Model for referencing repository where the device serve could be found"""
    # TODO: implement interface
    pass


class DeviceServerLicnese(models.Model):
    """Model for providing info about licencing of devcie servers."""
    # TODO: implement interface
    pass


class DeviceClass(models.Model):
    """Model to describe device classes implemented by device server"""
    # TODO: implement interface
    pass


class DeviceAttribute(models.Model):
    """Model for providing basic description of attribute"""
    # TODO: implement interface
    pass


class DeviceCommand(models.Model):
    """Model for providing basic description of attribute"""
    # TODO: implement interface
    pass


class DevicePipe(models.Model):
    """Model for providing basic description of attribute"""
    # TODO: implement interface
    pass


class DeviceProperty(models.Model):
    """Model for providing basic description of attribute"""
    # TODO: implement interface
    pass

class DeviceAttributeInfo(models.Model):
    """Model for providing additional infos about attributes. For future extenstion."""

    pass
