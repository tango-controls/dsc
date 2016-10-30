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



DS_COMMAND_DATATYPES = {
    'BooleanType': 'DevBoolean',
    'FloatType': 'DevFloat',
    'DoubleType': 'DevDouble',
    'IntType': 'DevLong',
    'LongType': 'DevLong64',
    'ShortType': 'DevShort',
    'StringType': 'DevString',
    'UIntType': 'DevULong',
    'ULongType': 'DevULong64',
    'UShortType': 'DevUShort',
    'UCharType': 'DevUChar',
    'CharType': 'DevChar',
    'CharArrayType': 'DevVarCharArray',
    'DoubleArrayType': 'DevVarDoubleArray',
    'DoubleStringArrayType': 'DevVarDoubleStringArray',
    'FloatArrayType': 'DevVarFloatArray',
    'LongArrayType': 'DevVarLong64Array',
    'IntArrayType': 'DevVarLongArray',
    'LongStringArrayType': 'DevVarLongStringArray',
    'ShortArrayType': 'DevVarShortArray',
    'StringArrayType': 'DevVarStringArray',
    'ULongArrayType': 'DevVarULong64Array',
    'UIntArrayType': 'DevVarULongArray',
    'UShortArrayType': 'DevVarUShortArray'
}


DS_ATTRIBUTE_DATATYPES = {
    'BooleanType': 'DevBoolean',
    'FloatType': 'DevFloat',
    'DoubleType': 'DevDouble',
    'IntType': 'DevLong',
    'LongType': 'DevLong64',
    'ShortType': 'DevShort',
    'StringType': 'DevString',
    'UIntType': 'DevULong',
    'ULongType': 'DevULong64',
    'UShortType': 'DevUShort',
    'UCharType': 'DevUChar',
    'CharType': 'DevChar',
}

# TODO extend class Content from tango if needed
###############################################################################################
@python_2_unicode_compatible
class DeviceServer(models.Model): #tango Content, chaged from models.Model
    """Model for a DeviceServer basic entities."""
    # TODO: implement interface

    name = models.CharField(
        max_length=64,
        verbose_name = 'Device Server')

    # TODO: check if it is necessery. It makes trouble upon migration
    # slug = models.SlugField(
    #     verbose_name=('slug'),
    #     max_length=250,
    #     unique=True,)

    description = models.TextField(verbose_name='Description')

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
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when license is removed from the system
        related_name='licensed_device_servers',
        blank=True, null=True,
        verbose_name='License')

    status = models.CharField(
        verbose_name='Status',
        max_length=10,
        # choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    # objects = ObjectManager()
    #
    # class QuerySet(
    #     models.query.QuerySet,
    # ):
    #     pass

    # TODO
    # class Meta:
    #     app_label = 'dsc'
    #     verbose_name = 'device server'
    #     verbose_name_plural = 'device servers'
        # ordering = [ 'name', ]

        #TODO add special permissions, verbose names

        # permissions = (
        #     ('view_device_servers', _('view (all) device servers')),
        #     ('view_published_structure', _('view published institutions')),
        #     ('view_mine_draft_structure', _('view my draft institutions')),
        #     ('change_mine_draft_structure', _('change my draft institutions')),
        #     ('publish_structure', _('(un)publish institutions')),
        # )
        #
        #
        # verbose_names = {
        #     'masculine': True,
        #     'undefined_sing': _('a device server'),
        #     'undefined_plur': _('device servers'),
        #     'defined_sing': _("the device server"),
        #     'defined_plur': _('the device servers'),
        # }


    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self, pk):
        #return '/dsc/%d' % self.pk
        return reverse('deviceserver_detail', kwargs={'pk': self.pk})  #args=[self.pk]

    def no_downloads(self):
        return self.activities.filter(activity_type = DS_ACTIVITY_DOWNLOAD).count()

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

    def downloads(self):
       down = self.activity_type.DS_ACTIVITY_DOWNLOAD.count() #returns count of downloads
       return down

    def __str__(self):
        return '%s' % self.activity_type

class DeviceServerDocumentation(models.Model):
    """Model for providing reference to device server documentation."""
    documentation_type = models.SlugField(verbose_name='Documentation type',
                                          choices=zip(['README', 'Manual', 'InstGuide',
                                                       'Generated', 'SourceDoc'],
                                                      ['README', 'Manual', 'Installation Guide',
                                                       'Generated', 'Source Documentation']
                                                      ))
    url = models.URLField(verbose_name='URL')
    device_server = models.ForeignKey(DeviceServer, related_name='documentation')

    def __str__(self):
        return '%s' % self.url

class DeviceServerRepository(models.Model):
    """Model for referencing repository where the device serve could be found"""
    repository_type = models.SlugField(
        verbose_name ='Repository Type',
        choices=zip(['GIT', 'SVN', 'Mercurial', 'FTP', 'Other'],
                    ['GIT', 'SVN', 'Mercurial', 'FTP', 'Other'])
    )
    url = models.URLField(verbose_name='URL')
    path_in_repository = models.CharField(max_length=255, verbose_name='Path', blank=True, default='')
    device_server = models.OneToOneField(DeviceServer, related_name='repository')


    def __str__(self):
        return '%s' % self.url

class DeviceServerLicense(models.Model):
    """Model for providing info about licencing of devcie servers."""
    name = models.CharField(primary_key=True, max_length=64, verbose_name='License')
    description = models.TextField(verbose_name='Description', blank=True, null=True, default='')
    url = models.URLField(blank=True, verbose_name='URL', null=True)

    def __str__(self):
        return '%s' % self.name

class DeviceClass(models.Model):
    """Model to describe device classes implemented by device server"""
    name =models.CharField(max_length=64, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    device_server = models.ForeignKey(DeviceServer,related_name='device_classes')
    license = models.ForeignKey(
        'DeviceServerLicense',
        editable=True,
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when license is removed from the system
        related_name='licensed_device_classes',
        blank=True, null=True,
        verbose_name='License')
    class_copyright = models.CharField(max_length=128, verbose_name="Copyright", default='')
    language = models.CharField(max_length=32,
                                choices=zip(['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView'],
                                            ['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView']),
                                verbose_name='Language', default='Cpp')


    def __str__(self):
        return '%s' % self.name

class DeviceClassInfo(models.Model):
    """Model for information about device server."""
    device_class = models.OneToOneField(DeviceClass, related_name='info')
    xmi_file = models.CharField(max_length=128) # this will store a link to source xmi_file
    contact_email = models.EmailField(verbose_name='Contact')
    class_family = models.CharField(max_length=64, blank=True, null=True, default='')  # TODO: implement class family choices
    platform = models.CharField(max_length=64,
                                choices=zip(['Windows','Unix Like', 'All Platforms'],
                                            ['Windows', 'Unix Like', 'All Platforms']),
                                verbose_name='Platform', default='All Platforms')
    bus = models.CharField(max_length=64, verbose_name='Bus', blank=True, null=True)  # TODO: implement bus choices
    manufacturer = models.CharField(max_length=64,verbose_name='Manufacturer',default='', null=True)  # at the beginning there will
                                                                                # not be any manufacturer table
    key_words = models.CharField(max_length=255, verbose_name="Key words", blank=True, null=True)
    product_reference = models.CharField(max_length=64, verbose_name="Product", default='')

    def __str__(self):
        return '%s' % self.device_class

class DeviceAttribute(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    attribute_type = models.SlugField(choices=zip(['Scalar','Spectrum','Image'],['Scalar','Spectrum','Image']),
                                      verbose_name='Type', default='Scalar')
    data_type = models.SlugField(choices=zip(DS_ATTRIBUTE_DATATYPES.values(),DS_ATTRIBUTE_DATATYPES.values()),
                                 verbose_name='Data Type', default='DevString')
    device_class = models.ForeignKey(DeviceClass, related_name='attributes')

    def __str__(self):
        return '%s' % self.name

class DeviceCommand(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64,verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    input_type = models.SlugField(choices=zip(DS_COMMAND_DATATYPES.values(),DS_COMMAND_DATATYPES.values()),
                                  verbose_name='Argument Type')
    output_type = models.SlugField(choices=zip(DS_COMMAND_DATATYPES.values(),DS_COMMAND_DATATYPES.values()),
                                   verbose_name='Output Type')
    device_class = models.ForeignKey(DeviceClass, related_name='commands')

    def __str__(self):
        return '%s' % self.name

class DevicePipe(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True)
    device_class = models.ForeignKey(DeviceClass, related_name='pipes')

    def __str__(self):
        return '%s' % self.name

class DeviceProperty(models.Model):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True)
    property_type = models.SlugField(choices=zip(DS_ATTRIBUTE_DATATYPES.values(),DS_ATTRIBUTE_DATATYPES.values()),
                                     verbose_name='Type')
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
        verbose_name = 'Device Servers Catalogue plugin'
