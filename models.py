from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from webu.models import LastPublishedObjectPluginBase, ObjectManager
from tango.models import Content
from django.utils.encoding import python_2_unicode_compatible
from webu.custom_models.registry import custom_model
from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

#Device Server statuses

STATUS_NEW = 'new'
STATUS_UPDATED = 'updated'
STATUS_CERTIFIED= 'certified'
STATUS_ARCHIVED = 'archived'
STATUS_DELETED = 'deleted'
STATUS_CHOICES = (
    (STATUS_NEW, ('New')),
    (STATUS_UPDATED, ('Updated')),
    (STATUS_CERTIFIED, ('Certified')),
    (STATUS_ARCHIVED, ('Archived')),
    (STATUS_DELETED, ('Deleted')),
)

#List of Device Servers activities
#TODO fill list, do we add subactivites of edit like import form, add attribute etc
DS_ACTIVITY_ADD = 'add'
DS_ACTIVITY_EDIT = 'edit'
DS_ACTIVITY_DOWNLOAD = 'download'
DS_ACTIVITY_DELETE = 'delete'
DS_ACTIVITY_APPLY_FOR_CERT = 'apply_for_cert'
DS_ACTIVITY_CERTIFY = 'certify'
DS_ACTIVITY_CHOICES = (
    (DS_ACTIVITY_ADD, ('Add')),
    (DS_ACTIVITY_EDIT, ('Edit')),
    (DS_ACTIVITY_DOWNLOAD, ('Download')),
    (DS_ACTIVITY_DELETE, ('Delete')),
    (DS_ACTIVITY_APPLY_FOR_CERT, ('Apply for cerification')),
    (DS_ACTIVITY_CERTIFY, ('Certify')),
)

# TODO extend class Content from tango if needed
###############################################################################################
@python_2_unicode_compatible
class DeviceServer(models.Model): #tango Content, chaged from models.Model
    """Model for a DeviceServer basic entities."""
    # TODO: implement interface

    name = models.CharField(
        max_length=64,
        verbose_name = ('Device Server'))

    slug = models.SlugField(
        verbose_name=('slug'),
        max_length=250,
        unique=True,)

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
        'DeviceServerLicense',
        editable=True,
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when user is removed from the system
        related_name='licensed_device_servers',
        blank=True, null=True,
        verbose_name=('License'))

    status = models.CharField(
        verbose_name=('Status'),
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,)

    objects = ObjectManager()

    class QuerySet(
        models.query.QuerySet,
    ):
        pass

    # TODO
    class Meta:
        app_label = 'dsc'
        verbose_name = ('device server')
        verbose_name_plural = ('device servers')
        ordering = [ 'name', ]

        #TODO add special permissions, verbose names
        '''
        permissions = (
            ('view_device_servers', _('view (all) device servers')),
            ('view_published_structure', _('view published institutions')),
            ('view_mine_draft_structure', _('view my draft institutions')),
            ('change_mine_draft_structure', _('change my draft institutions')),
            ('publish_structure', _('(un)publish institutions')),
        )


    verbose_names = {
        'masculine': True,
        'undefined_sing': _('a device server'),
        'undefined_plur': _('device servers'),
        'defined_sing': _("the device server"),
        'defined_plur': _('the device servers'),
    }
    '''

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self, pk):
        return '/dsc/%d' % self.pk
        #return reverse('deviceserver_detail', kwargs={'slug': self.slug})  #args=[self.pk]

###############################################################################################

class DeviceServerActivity(models.Model):
    """Model for tracking of activity around Device Server."""
    activity_type = models.CharField(
        verbose_name=('Activity'),
        max_length=10,
        choices=DS_ACTIVITY_CHOICES,)

    activity_info = models.TextField()

    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        editable=False,
        on_delete=models.SET_NULL, # important to avoid deletion of entries when user is removed from the system
        related_name='device_servers_activities',
        blank=True, null=True,)

    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True)

    device_server = models.ForeignKey(DeviceServer, related_name='activities')

    #TODO downloads counter
    def downloads(self):
       down = self.activity_type.DS_ACTIVITY_DOWNLOAD.count() #returns count of downloads
       return down

    def __str__(self):
        return '%s' % self.activity_type

class DeviceServerDocumentation(models.Model):
    """Model for providing reference to device server documentation."""
    documentation_type = models.SlugField()  # TODO: implement documentation type choices
    url = models.URLField()
    device_server = models.ForeignKey(DeviceServer, related_name='documentation')

    def __str__(self):
        return '%s' % self.url

class DeviceServerRepository(models.Model):
    """Model for referencing repository where the device serve could be found"""
    repository_type = models.SlugField(
        verbose_name ='Repository',
    )  # TODO: implement repository types choices
    url = models.URLField()
    path_in_repository = models.CharField(max_length=255)
    device_server = models.OneToOneField(DeviceServer, related_name='repository')


    def __str__(self):
        return '%s' % self.url

class DeviceServerLicense(models.Model):
    """Model for providing info about licencing of devcie servers."""
    name = models.CharField(primary_key=True, max_length=64)
    description = models.TextField()
    url = models.URLField(blank=True)

    def __str__(self):
        return '%s' % self.name

class DeviceClass(models.Model):
    """Model to describe device classes implemented by device server"""
    name =models.CharField(max_length=64)
    description = models.TextField()
    device_server = models.ForeignKey(DeviceServer,related_name='device_classes')

    def __str__(self):
        return '%s' % self.name

class DeviceClassInfo(models.Model):
    """Model for information about device server."""
    device_class = models.OneToOneField(DeviceClass, related_name='info')
    xmi_file = models.CharField(max_length=128) # this will store a link to source xmi_file
    contact_email = models.EmailField()
    class_family = models.CharField(max_length=64)  # TODO: implement class family choices
    platform = models.CharField(max_length=64)  # TODO: implement platform choices
    bus = models.CharField(max_length=64)  # at the beginning there will not be a manufacturer table, TODO: implement bus choices
    manufacturer = models.CharField(max_length=64)  # at the beginning there will not be a manufacturer table
    key_words = models.SlugField()

    def __str__(self):
        return '%s' % self.device_class

class DeviceAttribute(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64)
    description = models.TextField()
    attribute_type = models.SlugField()  # TODO: implement choice of attr type
    data_type = models.SlugField()  # TODO: implement choice of attr data type
    device_class = models.ForeignKey(DeviceClass, related_name='attributes')

    def __str__(self):
        return '%s' % self.name

class DeviceCommand(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64)
    description = models.TextField()
    input_type = models.SlugField()  # TODO: implement choice of cmd input type
    output_type = models.SlugField()  # TODO: implement choice of cmd output type
    device_class = models.ForeignKey(DeviceClass, related_name='commands')

    def __str__(self):
        return '%s' % self.name

class DevicePipe(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64)
    description = models.TextField()
    device_class = models.ForeignKey(DeviceClass, related_name='pipes')

    def __str__(self):
        return '%s' % self.name

class DeviceProperty(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64)
    description = models.TextField()
    property_type = models.SlugField()  # TODO: implement choice of property type
    device_class = models.ForeignKey(DeviceClass, related_name='properties')

    def __str__(self):
        return '%s' % self.name

class DeviceAttributeInfo(models.Model):
    """Model for providing additional infos about attributes. For future extenstion."""
    device_attribute = models.OneToOneField(DeviceAttribute,related_name='attribute_info')
    # TODO: implement extended interface of DeviceAttributeInfo

    def __str__(self):
        return '%s' % self.device_attribute

###############################################################################################

class DeviceServerPluginModel(CMSPlugin): #LastPublishedObjectPluginBase
    model = DeviceServer
    #TODO prepare plugin for administration CMS
    class Meta:
        app_label = 'dsc'
        verbose_name = ('Device Servers Catalogue plugin')
