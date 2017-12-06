import urllib2
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse
from webu.models import LastPublishedObjectPluginBase, ObjectManager
from tango.models import Content
from django.utils.encoding import python_2_unicode_compatible
from webu.custom_models.registry import custom_model
from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

# Device Server statuses
STATUS_NEW = 'new'
STATUS_VERIFIED = 'verified'
STATUS_UPDATED = 'updated'
STATUS_CERTIFIED= 'certified'
STATUS_ARCHIVED = 'archived'
STATUS_DELETED = 'deleted'
STATUS_CHOICES = (
    (STATUS_NEW, 'New'),
    (STATUS_VERIFIED, 'Verified'),
    (STATUS_UPDATED, 'Updated'),
    (STATUS_CERTIFIED, 'Certified'),
    (STATUS_ARCHIVED, 'Archived'),
    (STATUS_DELETED, 'Deleted'),
)

# Device Server statuses
DEV_STATUS_NEW = 'new'
DEV_STATUS_RELEASED = 'released'
DEV_STATUS_MAINTENANCE = 'maintenance'
DEV_STATUS_BROKEN = 'broken'
DEV_STATUS_CHOICES = (
    (DEV_STATUS_NEW, 'New development'),
    (DEV_STATUS_RELEASED, 'Released'),
    (DEV_STATUS_MAINTENANCE, 'In maintenance'),
    (DEV_STATUS_BROKEN, 'Broken'),
)

# List of Device Servers activities
# TODO fill list, do we add subactivites of edit like import form, add attribute etc
DS_ACTIVITY_ADD = 'add'
DS_ACTIVITY_EDIT = 'edit'
DS_ACTIVITY_DOWNLOAD = 'download'
DS_ACTIVITY_DELETE = 'delete'
DS_ACTIVITY_APPLY_FOR_CERT = 'apply_for_cert'
DS_ACTIVITY_CERTIFY = 'certify'
DS_ACTIVITY_VERIFICATION = 'verify'
DS_ACTIVITY_REVERT = 'revert'
DS_ACTIVITY_CHOICES = (
    (DS_ACTIVITY_ADD, 'Create'),
    (DS_ACTIVITY_EDIT, 'Update'),
    (DS_ACTIVITY_DOWNLOAD, 'Download'),
    (DS_ACTIVITY_DELETE, 'Delete'),
    (DS_ACTIVITY_APPLY_FOR_CERT, 'Apply for certification'),
    (DS_ACTIVITY_CERTIFY, 'Certificate'),
    (DS_ACTIVITY_VERIFICATION, 'Verify'),
    (DS_ACTIVITY_VERIFICATION, 'Revert'),
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
    'UShortArrayType': 'DevVarUShortArray',
    'VoidType': 'DevVoid',
    'ConstStringType': 'ConstDevString',
    'StateType': 'State'
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
    'EncodedType': 'DevEncoded',
    'StateType': 'DevState'
}

DS_PROPERTIES_DATATYPES = {
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
    'BooleanVectorType': 'Array of DevBoolean',
    'FloatVectorType': 'Array of DevFloat',
    'DoubleVectorType': 'Array of DevDouble',
    'IntVectorType': 'Array of DevLong',
    'LongVectorType': 'Array of DevLong64',
    'ShortVectorType': 'Array of DevShort',
    'StringVectorType': 'Array of DevString',
    'UIntVectorType': 'Array of DevULong',
    'ULongVectorType': 'Array of DevULong64',
    'UShortVectorType': 'Array of DevUShort',
    'UCharVectorType': 'Array of DevUChar',
    'CharVectorType': 'Array of DevChar',

}


class DscManagedModel(models.Model):

    # objects in the database are not deleted but invalidated
    invalidate_activity = models.ForeignKey('DeviceServerActivity',
                                            related_name='invalidated_%(class)s',
                                            default=None, null=True, blank=True)

    # if object is changed it is marked as
    last_update_activity = models.ForeignKey('DeviceServerActivity',
                                             related_name='updated_%(class)s',
                                             default=None, null=True, blank=True)

    create_activity = models.ForeignKey('DeviceServerActivity',
                                        related_name='created_%(class)s',
                                        default=None, null=True, blank=True)

    def is_valid(self):
        if self.invalidate_activity is None:
            return True
        else:
            return False

    def make_invalid(self, activity):
        """ Invalidate the object and return invalidate object"""
        self.invalidate_activity = activity
        return self

    def is_deleted(self):
        return not self.is_valid()

    def is_updated(self):
        if self.last_update_activity is None:
            return False
        else:
            return True

    def last_update_method(self):
        create_object = None
        if self.last_update_activity is not None and hasattr(self.last_update_activity, 'create_object'):
            create_object = self.last_update_activity.create_object
        elif self.create_activity is not None and hasattr(self.create_activity, 'create_object'):
            create_object = self.create_activity.create_object

        if create_object is not None and create_object.all().count() > 0:
            if create_object.first().use_uploaded_xmi_file:
                return 'file'
            elif create_object.first().use_url_xmi_file:
                return 'url'
        return 'manual'

    def updated_by_script(self):
        create_object = None
        if self.last_update_activity is not None and hasattr(self.last_update_activity, 'create_object'):
            create_object = self.last_update_activity.create_object
        elif self.create_activity is not None and hasattr(self.create_activity, 'create_object'):
            create_object = self.create_activity.create_object

        if create_object is not None and create_object.all().count() > 0:
            return create_object.first().script_operation
        return False

    def delete(self, activity=None, user=None):
        if activity is None:
            activity = DeviceServerActivity(
                activity_type=DS_ACTIVITY_DELETE,
                activity_info='%s has been deleted.' % self.__str__(),
                created_by=user
            )
        activity.device_server = self.device_server
        activity.save()
        self.make_invalid(activity)
        self.save()

    class Meta:
        abstract = True


@python_2_unicode_compatible
class DeviceServer(DscManagedModel):
    """Model for a DeviceServer basic entities."""

    name = models.CharField(
        max_length=128,
        verbose_name='Device Server')

    description = models.TextField(verbose_name='Description')

    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        editable=False,
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when user is removed from the system
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
        verbose_name='Information status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    development_status = models.CharField(
        verbose_name='Development status',
        max_length=20,
        choices=DEV_STATUS_CHOICES,
        default=DEV_STATUS_NEW,
        blank=True
    )

    certified = models.BooleanField(
        verbose_name='Certified',
        default=False,
        blank=True
    )

    readme = models.FileField(verbose_name='Readme', upload_to='dsc_readmes', null=True, blank=True, max_length=100000)

    picture = models.ImageField(verbose_name="Picture",
                                upload_to='dsc_pictures',
                                null=True,
                                blank=True,
                                max_length=1024*1024)

    class Meta:
        permissions = (
            ('admin_deviceserver', 'do various administration tasks on device servers'),
            ('update_own_deviceserver', 'do changes to device server for creator'),
            ('delete_own_deviceserver', 'deletion of device server for creator'),
        )

    # TODO add verbose names

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
        if self.is_valid():
            return '%s' % self.name
        else:
            return 'invalidated-%s' % self.name

    def get_absolute_url(self, pk):
        return reverse('deviceserver_detail', kwargs={'pk': self.pk})

    def no_downloads(self):
        return self.activities.filter(activity_type=DS_ACTIVITY_DOWNLOAD).count()

    def manufacturers(self):
        mfs = []
        for cl in self.device_classes.all():
            m = cl.info.manufacturer
            if m != '' and m is not None and m not in mfs:
                mfs.append(m)

        return '; '.join(mfs)

    def products(self):
        mfs = []
        for cl in self.device_classes.all():
            m = cl.info.product_reference
            if m != '' and m is not None and m not in mfs:
                mfs.append(m)

        return '; '.join(mfs)

    def family(self):
        mfs = []
        for cl in self.device_classes.all():
            m = cl.info.class_family
            if m != '' and m is not None and m not in mfs:
                mfs.append(m)

        return '; '.join(mfs)

    def make_backup(self, activity):
        # for device server

        backup_ds = DeviceServer(name=self.name, description=self.description,
                                 license=self.license,
                                 created_by=self.created_by,
                                 created_at=self.created_at,
                                 status=self.status,
                                 last_update_activity=self.last_update_activity,
                                 create_activity=self.create_activity,
                                 invalidate_activity=activity,
                                 development_status=self.development_status,
                                 certified=self.certified,
                                 readme=self.readme,
                                 picture=self.picture
                                 )
        return backup_ds

###############################################################################################


class DeviceServerActivity(models.Model):
    """Model for tracking of activity around Device Server."""

    activity_type = models.CharField(
        verbose_name='Activity',
        max_length=10,
        choices=DS_ACTIVITY_CHOICES)

    activity_info = models.TextField()

    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        editable=False,
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when user is removed from the system
        related_name='device_servers_activities',
        blank=True, null=True,)

    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True)

    device_server = models.ForeignKey(DeviceServer, related_name='activities', null=True, blank=True)

    device_server_backup = models.ForeignKey(DeviceServer, related_name='backup_for', null=True, blank=True)

    def downloads(self):
        """Return number of downloads"""
        down = self.activity_type.DS_ACTIVITY_DOWNLOAD.count()
        return down

    def __str__(self):
        if self.device_server is None:
            return '%s ' % self.activity_type
        else:
            return '%s %s' % (self.activity_type, self.device_server.name)


class DeviceServerDocumentation(DscManagedModel):
    """Model for providing reference to device server documentation."""

    documentation_type = models.SlugField(verbose_name='Documentation type',
                                          choices=zip(['README', 'Manual', 'InstGuide',
                                                       'Generated', 'SourceDoc'],
                                                      ['README', 'Manual', 'Installation Guide',
                                                       'Generated', 'Source Documentation']
                                                      ))

    title = models.CharField(max_length=255,
                             blank=True,
                             null=True,
                             default='',
                             verbose_name='Title')

    documentation_file = models.FileField(verbose_name='Document',
                                          upload_to='dsc_readmes',
                                          null=True,
                                          blank=True,
                                          max_length=2000000
                                          )

    url = models.URLField(verbose_name='URL', null=True, blank=True, default='')

    device_server = models.ForeignKey(DeviceServer, related_name='documentation')

    def get_documentation_url(self):
        if self.documentation_file is not None and hasattr(self.documentation_file, 'url'):
            return self.documentation_file.url
        else:
            return self.url

    def __str__(self):
        return '%s: %s' % (self.title, self.get_documentation_url)


class DeviceServerRepository(DscManagedModel):
    """Model for referencing repository where the device serve could be found"""

    repository_type = models.SlugField(
        verbose_name='Repository Type',
        choices=zip(['GIT', 'SVN', 'Mercurial', 'FTP', 'Other'],
                    ['GIT', 'SVN', 'Mercurial', 'FTP', 'Other']),
        null=True,
        blank=True
    )

    url = models.URLField(verbose_name='URL', null=True, blank=True)

    path_in_repository = models.CharField(max_length=255, verbose_name='Path', blank=True, default='')

    contact_email = models.EmailField(verbose_name='Please write to', blank=True, null=True, default='')

    download_url = models.URLField(verbose_name='Download URL', null=True, blank=True)

    tag = models.CharField(verbose_name='Tag', max_length=128, blank=True, null=True, default='')

    device_server = models.OneToOneField(DeviceServer, related_name='repository', null=True)

    def __str__(self):
        return '%s' % self.url


class DeviceServerLicense(models.Model):
    """Model for providing info about licencing of device servers."""

    name = models.CharField(primary_key=True, max_length=64, verbose_name='License')

    description = models.TextField(verbose_name='Description', blank=True, null=True, default='')

    url = models.URLField(blank=True, verbose_name='URL', null=True)

    def __str__(self):
        return '%s' % self.name


class DeviceClass(DscManagedModel):
    """Model to describe device classes implemented by device server"""

    name = models.CharField(max_length=128, verbose_name='Name')

    description = models.TextField(verbose_name='Description', blank=True, null=True)

    device_server = models.ForeignKey(DeviceServer, related_name='device_classes')

    license = models.ForeignKey(
        'DeviceServerLicense',
        editable=True,
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when license is removed from the system
        related_name='licensed_device_classes',
        blank=True,
        null=True,
        verbose_name='License')

    class_copyright = models.CharField(max_length=255, verbose_name="Copyright", default='', blank=True)

    language = models.CharField(max_length=32,
                                choices=zip(['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView'],
                                            ['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView']),
                                verbose_name='Language', default='Cpp')

    def __str__(self):
        if self.is_valid():
            return '%s' % self.name
        else:
            return 'invalidated-%s' % self.name

    def make_backup(self, activity):
        clo = DeviceClass()
        clo.name = self.name
        clo.description = self.description
        clo.class_copyright = self.class_copyright
        clo.language = self.language
        clo.create_activity = self.create_activity
        clo.last_update_activity = self.last_update_activity
        clo.make_invalid(activity)
        clo.device_server = self.device_server

        return clo


class DeviceClassFamily(DscManagedModel):
    """Model to store additional families for classes"""

    family = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return '%s' % self.family


class DeviceClassInfo(DscManagedModel):
    """Model for information about device server."""

    device_class = models.OneToOneField(DeviceClass, related_name='info')

    xmi_file = models.CharField(max_length=128, blank=True, null=True)  # this will store a link to source xmi_file

    contact_email = models.EmailField(verbose_name='Contact')

    class_family = models.CharField(max_length=128, blank=True, null=True, default='')  # TODO: implement choices

    platform = models.CharField(max_length=64,
                                choices=zip(['Windows', 'Unix Like', 'All Platforms'],
                                            ['Windows', 'Unix Like', 'All Platforms']),
                                verbose_name='Platform', default='All Platforms')

    bus = models.CharField(max_length=128, verbose_name='Bus', blank=True, null=True)  # TODO: implement bus choices

    manufacturer = models.CharField(max_length=128, verbose_name='Manufacturer', default='', null=True)

    key_words = models.CharField(max_length=255, verbose_name="Key words", blank=True, null=True)

    product_reference = models.CharField(max_length=255, verbose_name="Product", default='')

    additional_families = models.ManyToManyField(DeviceClassFamily, related_name='device_class_infos', blank=True)

    def all_families(self):
        families = [self.class_family, ] + [dcf.family for dcf in self.additional_families]
        return set(families)

    def make_backup(self, activity, cl=None):
        cli = DeviceClassInfo()
        if cl is None:
            cli.device_class = self.device_class
        else:
            cli.device_class = cl
        cli.contact_email = self.contact_email
        cli.class_family = self.class_family
        cli.platform = self.platform
        cli.bus = self.bus
        cli.manufacturer = self.manufacturer
        cli.product_reference = self.product_reference
        cli.key_words = self.key_words
        cli.create_activity = self.create_activity
        cli.last_update_activity = self.last_update_activity
        cli.invalidate_activity = activity
        cli.save()  # need to have an id to upfate many-to-many field
        cli.additional_families.add(*self.additional_families.all())

        return cli

    @property
    def device_server(self):
        return self.device_class.device_server

    def __str__(self):
        return '%s' % self.device_class


class DeviceAttribute(DscManagedModel):
    """Model for providing basic description of attribute"""

    name = models.CharField(max_length=64, verbose_name='Name')

    description = models.TextField(verbose_name='Description', blank=True, null=True)

    attribute_type = models.SlugField(choices=zip(['Scalar', 'Spectrum', 'Image'],
                                                  ['Scalar', 'Spectrum', 'Image']),
                                      verbose_name='Type', default='Scalar')

    data_type = models.SlugField(choices=zip(DS_ATTRIBUTE_DATATYPES.values(), DS_ATTRIBUTE_DATATYPES.values()),
                                 verbose_name='Data Type', default='DevString')

    device_class = models.ForeignKey(DeviceClass, related_name='attributes')

    @property
    def device_server(self):
        return self.device_class.device_server

    def __str__(self):
        return '%s' % self.name


class DeviceCommand(DscManagedModel):
    """Model for providing basic description of commands"""

    name = models.CharField(max_length=64, verbose_name='Name')

    description = models.TextField(verbose_name='Description', blank=True, null=True)

    input_type = models.SlugField(choices=zip(DS_COMMAND_DATATYPES.values(),
                                              DS_COMMAND_DATATYPES.values()),
                                  verbose_name='Argument Type', blank=True, null=True)

    input_description = models.TextField(verbose_name='Argin description', blank=True, null=True)

    output_type = models.SlugField(choices=zip(DS_COMMAND_DATATYPES.values(),
                                               DS_COMMAND_DATATYPES.values()),
                                   verbose_name='Output Type', blank=True, null=True)

    output_description = models.TextField(verbose_name='Argout description', blank=True, null=True)

    device_class = models.ForeignKey(DeviceClass, related_name='commands')

    @property
    def device_server(self):
        return self.device_class.device_server

    def __str__(self):
        return '%s' % self.name


class DevicePipe(DscManagedModel):
    """Model for providing basic description of pipes"""

    name = models.CharField(max_length=64, verbose_name='Name')

    description = models.TextField(verbose_name='Description', blank=True)

    device_class = models.ForeignKey(DeviceClass, related_name='pipes')

    @property
    def device_server(self):
        return self.device_class.device_server

    def __str__(self):
        return '%s' % self.name


class DeviceProperty(DscManagedModel):
    """Model for providing basic description of properties"""

    name = models.CharField(max_length=64, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True)
    property_type = models.SlugField(verbose_name='Type')
    is_class_property = models.BooleanField(verbose_name='Class property', blank=True, default=False)
    device_class = models.ForeignKey(DeviceClass, related_name='properties')

    @property
    def device_server(self):
        return self.device_class.device_server

    def __str__(self):
        return '%s' % self.name


class DeviceAttributeInfo(DscManagedModel):
    """Model for providing additional infos about attributes. For future extenstion."""

    device_attribute = models.OneToOneField(DeviceAttribute,related_name='attribute_info')

    # TODO: implement extended interface of DeviceAttributeInfo
    def __str__(self):
        return '%s' % self.device_attribute

###############################################################################################

from xmi_parser import TangoXmiParser


class DeviceServerAddModel(models.Model):
    """This model is used to provide form and optionally do background processing"""

    ds_info_copy = models.BooleanField(verbose_name='Guess device server name and description from class info?',
                                       blank=True, default=True)

    script_operation = models.BooleanField(verbose_name='Updated with script?',
                                           blank=True, default=False)

    name = models.CharField(max_length=64, verbose_name='Device server name', blank=True, default='')

    description = models.TextField(verbose_name='Description', blank=True, default='')

    development_status = models.CharField(
        verbose_name='Development status',
        max_length=20,
        choices=DEV_STATUS_CHOICES,
        default=DEV_STATUS_NEW,
        blank=True
    )

    certified = models.BooleanField(
        verbose_name='Certified',
        default=False,
        blank=True,
    )

    ds_status = models.CharField(
        verbose_name='Information status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    picture = models.ImageField(verbose_name="Picture",
                                upload_to='dsc_pictures',
                                null=True,
                                blank=True,
                                max_length=1024 * 1024)

    # repository
    process_from_repository = models.BooleanField(verbose_name='Use repository only', blank=True, default=False)

    available_in_repository = models.BooleanField(verbose_name='Available in repository', default=True)

    repository_type = models.SlugField(
        verbose_name='Repository Type',
        choices=zip(['GIT', 'SVN', 'Mercurial', 'FTP', 'Other'],
                    ['GIT', 'SVN', 'Mercurial', 'FTP', 'Other']),
        blank=True, default=''
    )

    repository_url = models.URLField(verbose_name='Repository URL', blank=True, default='')

    repository_path = models.CharField(max_length=255, verbose_name='Path within reposiroty', blank=True, default='')

    repository_contact = models.EmailField(verbose_name='Please write to', blank=True, null=True, default='')

    repository_download_url = models.URLField(verbose_name='Dwonload URL', blank=True, default='')

    repository_tag = models.CharField(verbose_name='Tag', max_length=128, blank=True, null=True, default='')

    # documentation
    upload_readme = models.BooleanField(verbose_name='Upload README', blank=True, default=False)

    readme_file = models.FileField(verbose_name='README file', upload_to='dsc_readmes',
                                   blank=True, null=True, max_length=100000)

    other_documentation1 = models.BooleanField(verbose_name='Other documentation - 1', blank=True, default=False)

    documentation1_pk = models.IntegerField(blank=True, null=True)

    documentation1_type = models.SlugField(verbose_name='Documentation type',
                                           choices=zip(['README', 'Manual', 'InstGuide',
                                                       'Generated', 'SourceDoc'],
                                                       ['README', 'Manual', 'Installation Guide',
                                                       'Generated', 'Source Documentation']),
                                           null=True, blank=True)

    documentation1_url = models.URLField(verbose_name='URL', blank=True, null=True, default='')

    documentation1_title = models.CharField(max_length=255,
                                            blank=True,
                                            null=True,
                                            default='',
                                            verbose_name='Title')

    documentation1_file = models.FileField(verbose_name='Document',
                                           upload_to='dsc_readmes',
                                           null=True,
                                           blank=True,
                                           max_length=2000000)

    other_documentation2 = models.BooleanField(verbose_name='Other documentation - 2', blank=True, default=False)

    documentation2_pk = models.IntegerField(blank=True, null=True)

    documentation2_type = models.SlugField(verbose_name='Documentation type',
                                           choices=zip(['README', 'Manual', 'InstGuide',
                                                        'Generated', 'SourceDoc'],
                                                       ['README', 'Manual', 'Installation Guide',
                                                        'Generated', 'Source Documentation']
                                                       ), null=True, blank=True)

    documentation2_url = models.URLField(verbose_name='URL', blank=True, null=True, default='')

    documentation2_title = models.CharField(max_length=255,
                                            blank=True,
                                            null=True,
                                            default='',
                                            verbose_name='Title')

    documentation2_file = models.FileField(verbose_name='Document',
                                           upload_to='dsc_readmes',
                                           null=True,
                                           blank=True,
                                           max_length=2000000
                                           )

    other_documentation3 = models.BooleanField(verbose_name='Other documentation - 3', blank=True, default=False)

    documentation3_pk = models.IntegerField(blank=True, null=True)

    documentation3_type = models.SlugField(verbose_name='Documentation type',
                                           choices=zip(['README', 'Manual', 'InstGuide',
                                                        'Generated', 'SourceDoc'],
                                                       ['README', 'Manual', 'Installation Guide',
                                                        'Generated', 'Source Documentation']
                                                       ), null=True, blank=True)

    documentation3_url = models.URLField(verbose_name='URL', blank=True, null=True, default='')

    documentation3_title = models.CharField(max_length=255,
                                            blank=True,
                                            null=True,
                                            default='',
                                            verbose_name='Title')

    documentation3_file = models.FileField(verbose_name='Document',
                                           upload_to='dsc_readmes',
                                           null=True,
                                           blank=True,
                                           max_length=2000000
                                           )

    # xmi file
    use_uploaded_xmi_file = models.BooleanField(verbose_name='Upload .xmi file to populate database.',
                                                blank=True,
                                                default=True)

    add_class = models.BooleanField(
        verbose_name='Add new class to the device server instead of updating existing ones?',
        blank=True,
        default=False)

    xmi_file = models.FileField(verbose_name='.XMI file',
                                upload_to='dsc_xmi_files',
                                blank=True,
                                null=True)

    use_url_xmi_file = models.BooleanField(verbose_name='Provide .xmi file URL populate database.',
                                           blank=True,
                                           default=False)

    xmi_file_url = models.URLField(verbose_name='XMI source URL', blank=True, null=True, default='')

    def xmi_string(self):
        """ This method returns .XMI string
            :return  (xmi_string, is_ok, error_message)
        """

        if hasattr(self, 'valid_xmi_string'):
            if self.valid_xmi_string is not None:
                return self.valid_xmi_string, True, ''
        try:
            if self.use_uploaded_xmi_file:
                if self.xmi_file.size < 10:
                    raise Exception('The .XMI file seems to be empty.')
                if self.xmi_file.size > 200000:
                    raise Exception('The file is to large to be a Tango .XMI file.')

                xmi_string = self.xmi_file.read()

            elif self.use_url_xmi_file:
                response = urllib2.urlopen(self.xmi_file_url)
                xmi_size = int(response.info().get('Content-Length', 0))
                if xmi_size < 10:
                    raise Exception('The .XMI file pointed by the url seems to be empty.')
                if xmi_size > 200000:
                    raise Exception('The .XMI file pointed by the url is to large to be a Tango .XMI file.')

                xmi_string = response.read()

            parser = TangoXmiParser(xml_string=xmi_string)

            is_valid, message = parser.is_valid()

            if not is_valid:
                print "Parsing problem: %s" % message
                raise Exception(message)

        except Exception as e:
            raise e

        return xmi_string, True, ''

    # manual info
    use_manual_info = models.BooleanField(verbose_name='Provide data manually', blank=True, default=False)

    class_name = models.CharField(max_length=64, verbose_name='Class name', blank=True, default='')

    class_description = models.TextField(verbose_name='Class description', blank=True, default='')

    contact_email = models.EmailField(verbose_name='Contact email', blank=True,default='')

    class_copyright = models.CharField(max_length=255, verbose_name="Copyright", default='', blank=True)

    language = models.CharField(max_length=32,
                                choices=zip(['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView'],
                                            ['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView']),
                                verbose_name='Language', default='Cpp', blank=True)

    class_family = models.CharField(max_length=128, blank=True, null=True, default='')  # TODO: implement choices

    additional_families = models.ManyToManyField(DeviceClassFamily, blank=True)

    platform = models.CharField(max_length=64,
                                choices=zip(['Windows', 'Unix Like', 'All Platforms'],
                                            ['Windows', 'Unix Like', 'All Platforms']),
                                verbose_name='Platform', default='All Platforms', blank=True)
    bus = models.CharField(max_length=128, verbose_name='Bus', blank=True, null=True)  # TODO: implement bus choices

    manufacturer = models.CharField(max_length=128, verbose_name='Manufacturer', default='', null=True, blank=True)

    key_words = models.CharField(max_length=255, verbose_name="Key words", blank=True, null=True, default='')

    product_reference = models.CharField(max_length=255, verbose_name="Product", default='', blank=True)

    license_name = models.CharField(max_length=64, verbose_name='License type', blank=True, default='GPL')

    # internal information
    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        editable=False,
        on_delete=models.SET_NULL,  # important to avoid deletion of entries when user is removed from the system
        related_name='device_servers_add_activities',
        blank=True, null=True,)

    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True)

    processed_ok = models.BooleanField(default=False)

    processed_with_errors = models.BooleanField(default=False)

    activity = models.ForeignKey('DeviceServerActivity',
                                 related_name='create_object',
                                 default=None, null=True)


class DeviceServerUpdateModel(DeviceServerAddModel):
    """Model for handling update form"""

    change_update_method = models.BooleanField(verbose_name='Change update method',
                                               blank=True,
                                               default=False)

    last_update_method = models.CharField(max_length=32,
                                          choices=zip(['manual', 'file', 'url'],
                                                      ['manual', 'file', 'url']),
                                          verbose_name='Previous update method: ', default='url', blank=True)

    def from_device_server(self, device_server, device_class=None):
        """ Fills fields based on device_server object"""

        assert isinstance(device_server, DeviceServer)

        self.name = device_server.name
        self.description = device_server.description
        self.readme_file = device_server.readme
        self.certified = device_server.certified
        self.ds_status = device_server.status
        self.development_status = device_server.development_status
        self.picture = device_server.picture

        self.last_update_method = device_server.last_update_method()

        if device_server.license is not None:
            self.license_name = device_server.license.name

        if hasattr(device_server, 'repository'):
            assert isinstance(device_server.repository, DeviceServerRepository)
            self.repository_type = device_server.repository.repository_type
            self.repository_contact = device_server.repository.contact_email
            self.repository_url = device_server.repository.url
            self.repository_download_url = device_server.repository.download_url
            self.repository_path = device_server.repository.path_in_repository
            self.repository_tag = device_server.repository.tag

        docs = device_server.documentation.filter(invalidate_activity=None).all().distinct()
        if docs.count() > 0:
            self.other_documentation1 = True
            self.documentation1_type = docs[0].documentation_type
            self.documentation1_title = docs[0].title
            self.documentation1_file = docs[0].documentation_file
            self.documentation1_url = docs[0].url
            self.documentation1_pk = docs[0].pk

        if docs.count() > 1:
            self.other_documentation2 = True
            self.documentation2_type = docs[1].documentation_type
            self.documentation2_title = docs[1].title
            self.documentation2_file = docs[1].documentation_file
            self.documentation2_url = docs[1].url
            self.documentation2_pk = docs[1].pk

        if docs.count() > 2:
            self.other_documentation3 = True
            self.documentation3_type = docs[2].documentation_type
            self.documentation3_title = docs[2].title
            self.documentation3_file = docs[2].documentation_file
            self.documentation3_url = docs[2].url
            self.documentation3_pk = docs[2].pk

        if device_class is None:
            cls = device_server.device_classes.all()
        else:
            cls = device_server.device_classes.filter(pk=device_class)

        self.ds_info_copy = False

        if len(cls) > 0:
            cl = cls[0]
            assert isinstance(cl, DeviceClass)
            self.class_copyright = cl.class_copyright
            self.class_description = cl.description
            self.class_name = cl.name
            self.language = cl.language
            if cl.license is not None:
                self.license_name = cl.license.name

            if self.name == self.class_name and ( self.description == self.class_description or self.description == ''):
                self.ds_info_copy = True

            self.class_family = cl.info.class_family
            self.manufacturer = cl.info.manufacturer
            self.product_reference = cl.info.product_reference
            self.platform = cl.info.platform
            self.bus = cl.info.bus
            self.key_words = cl.info.key_words
            self.contact_email = cl.info.contact_email

            self.save() # needs to do it to have pk
            self.additional_families.add(*cl.info.additional_families.all())

        return self


def filtered_device_servers(family=None, manufacturer=None, product=None, bus=None, key_words=None, user=None):
    """ Provides a filtered queryset of device servers"""

    q = DeviceServer.objects.filter(invalidate_activity=None)

    if manufacturer is not None:
        q = q.filter(device_classes__info__manufacturer__icontains=manufacturer)

    if product is not None:
        q = q.filter(device_classes__info__product_reference__icontains=product)

    if family is not None and len(family) > 0:
        q = q.filter(device_classes__info__class_family=family) | \
            q.filter(device_classes__info__additional_families__family__icontains=family)

    if bus is not None:
        q = q.filter(device_classes__info__bus__icontains=bus)

    if key_words is not None:
        q = q.filter(device_classes__info__key_words__icontains=key_words)

    if user is not None:
        q = q.filter(Q(device_classes__info__contact_email__istartswith=user) |
                     Q(repository__contact_email__istartswith=user) |
                     Q(device_classes__class_copyright__icontains=user) |
                     Q(activities__created_by__username__istartswith=user) |
                     Q(activities__created_by__first_name__istartswith=user) |
                     Q(activities__created_by__first_name__in=user.split()) |
                     Q(activities__created_by__last_name__istartswith=user) |
                     Q(activities__created_by__last_name__in=user.split()) |
                     Q(activities__created_by__email__istartswith=user)
                     )


    return q.filter(invalidate_activity=None)


def search_device_servers(search_text):
    """ Provides a filtered queryset of device servers"""

    q = DeviceServer.objects.filter(invalidate_activity=None).filter(device_classes__invalidate_activity=None)

    qn = q.filter(name__icontains=search_text) | q.filter(device_classes__name__icontains=search_text)

    qd = q.filter(description__icontains=search_text) | q.filter(device_classes__description__icontains=search_text)

    qm = q.filter(device_classes__info__manufacturer__icontains=search_text)

    qp = q.filter(device_classes__info__product_reference__icontains=search_text)

    qf = q.filter(device_classes__info__class_family__icontains=search_text) | \
            q.filter(device_classes__info__additional_families__family__icontains=search_text)

    qb = q.filter(device_classes__info__bus__icontains=search_text)

    qk = q.filter(device_classes__info__key_words__icontains=search_text)

    qall = qn | qd | qm | qp | qf | qb | qk

    return qall.filter(invalidate_activity=None).distinct()

###################################################################################


class DeviceServerPluginModel(CMSPlugin):
    model = DeviceServerActivity

    # TODO prepare plugin for administration CMS
    class Meta:
        app_label = 'dsc'
        verbose_name = 'Device Classes Catalogue plugin'


class DeviceServersActivityPluginModel(CMSPlugin):
    model = DeviceServer

    items_number = models.PositiveSmallIntegerField(verbose_name="Number of items", default=5)

    # TODO prepare plugin for administration CMS
    class Meta:
        app_label = 'dsc'
        verbose_name = 'Device Classes Catalogue Activity plugin'
