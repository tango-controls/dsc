import urllib2
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

    # TODO: implement interface
    name = models.CharField(
        max_length=64,
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
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    development_status = models.CharField(
        verbose_name='Development status',
        max_length=10,
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

    class Meta:
        permissions = (
            ('admin_deviceserver', 'do various administration tasks on device servers'),
            ('update_own_deviceserver', 'do changes to device server for creator'),
            ('delete_own_deviceserver', 'deletion of device server for creator'),
        )
    #     app_label = 'dsc'
    #     verbose_name = 'device server'
    #     verbose_name_plural = 'device servers'
    #     ordering = [ 'name', ]

    # TODO addverbose names


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
                                 certified=self.certified
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
    url = models.URLField(verbose_name='URL')
    device_server = models.ForeignKey(DeviceServer, related_name='documentation')

    def __str__(self):
        return '%s' % self.url


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
    """Model for providing info about licencing of devcie servers."""
    name = models.CharField(primary_key=True, max_length=64, verbose_name='License',
                            )
    description = models.TextField(verbose_name='Description', blank=True, null=True, default='')
    url = models.URLField(blank=True, verbose_name='URL', null=True)

    def __str__(self):
        return '%s' % self.name


class DeviceClass(DscManagedModel):
    """Model to describe device classes implemented by device server"""
    name = models.CharField(max_length=64, verbose_name='Name')
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
    class_copyright = models.CharField(max_length=128, verbose_name="Copyright", default='', blank=True)
    language = models.CharField(max_length=32,
                                choices=zip(['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView'],
                                            ['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView']),
                                verbose_name='Language', default='Cpp')
    # def make_invalid(self, activity):
    #    super(DeviceClass,self).make_invalid(activity)
    #    for attr in

    def __str__(self):
        return '%s' % self.name


class DeviceClassInfo(DscManagedModel):
    """Model for information about device server."""
    device_class = models.OneToOneField(DeviceClass, related_name='info')
    xmi_file = models.CharField(max_length=128, blank=True, null=True)  # this will store a link to source xmi_file
    contact_email = models.EmailField(verbose_name='Contact')
    class_family = models.CharField(max_length=64, blank=True, null=True, default='')  # TODO: implement choices
    platform = models.CharField(max_length=64,
                                choices=zip(['Windows', 'Unix Like', 'All Platforms'],
                                            ['Windows', 'Unix Like', 'All Platforms']),
                                verbose_name='Platform', default='All Platforms')
    bus = models.CharField(max_length=64, verbose_name='Bus', blank=True, null=True)  # TODO: implement bus choices
    manufacturer = models.CharField(max_length=64, verbose_name='Manufacturer', default='', null=True)
    # at the beginning there will not be any manufacturer table
    key_words = models.CharField(max_length=255, verbose_name="Key words", blank=True, null=True)
    product_reference = models.CharField(max_length=64, verbose_name="Product", default='')

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
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    input_type = models.SlugField(choices=zip(DS_COMMAND_DATATYPES.values(),
                                              DS_COMMAND_DATATYPES.values()),
                                  verbose_name='Argument Type',blank=True, null=True)
    input_description = models.TextField(verbose_name='Argin description', blank=True, null=True)
    output_type = models.SlugField(choices=zip(DS_COMMAND_DATATYPES.values(),
                                               DS_COMMAND_DATATYPES.values()),
                                   verbose_name='Output Type',blank=True, null=True)
    output_description = models.TextField(verbose_name='Argout description', blank=True, null=True)
    device_class = models.ForeignKey(DeviceClass, related_name='commands')

    @property
    def device_server(self):
        return self.device_class.device_server

    def __str__(self):
        return '%s' % self.name


class DevicePipe(DscManagedModel):
    """Model for providing basic description of attribute"""
    name = models.CharField(max_length=64, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True)
    device_class = models.ForeignKey(DeviceClass, related_name='pipes')

    @property
    def device_server(self):
        return self.device_class.device_server

    def __str__(self):
        return '%s' % self.name


class DeviceProperty(DscManagedModel):
    """Model for providing basic description of attribute"""
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


class DeviceServerAddModel(models.Model):
    """This model is used to provide form and optionally do background processing"""
    name = models.CharField(max_length=64, verbose_name='Device server name', blank=True, default='')
    description = models.TextField(verbose_name='Description', blank=True, default='')

    development_status = models.CharField(
        verbose_name='Development status',
        max_length=10,
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
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

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
    repository_download_url= models.URLField(verbose_name='Dwonload URL', blank=True, default='')

    # documentation
    upload_readme = models.BooleanField(verbose_name='Upload README', blank=True, default=False)
    readme_file = models.FileField(verbose_name='README file', upload_to='dsc_readmes',
                                   blank=True, null=True, max_length=100000)
    other_documentation1 = models.BooleanField(verbose_name='Link to other documentation', blank=True, default=False)
    documentation1_type = models.SlugField(verbose_name='Documentation type',
                                           choices=zip(['README', 'Manual', 'InstGuide',
                                                       'Generated', 'SourceDoc'],
                                                      ['README', 'Manual', 'Installation Guide',
                                                       'Generated', 'Source Documentation']
                                                      ), null=True, blank=True)
    documentation1_url = models.URLField(verbose_name='URL', blank=True, null=True, default='')

    other_documentation2 = models.BooleanField(verbose_name='Link to other documentation', blank=True, default=False)
    documentation2_type = models.SlugField(verbose_name='Documentation type',
                                           choices=zip(['README', 'Manual', 'InstGuide',
                                                        'Generated', 'SourceDoc'],
                                                       ['README', 'Manual', 'Installation Guide',
                                                        'Generated', 'Source Documentation']
                                                       ), null=True, blank=True)
    documentation2_url = models.URLField(verbose_name='URL', blank=True, null=True, default='')

    # xmi file
    use_uploaded_xmi_file = models.BooleanField(verbose_name='Upload .xmi file to populate database.',
                                                blank=True,
                                                default=True)
    xmi_file = models.FileField(verbose_name='.XMI file',
                                upload_to='dsc_xmi_files',
                                blank=True,
                                null=True)

    use_url_xmi_file = models.BooleanField(verbose_name='Provide .xmi file URL populate database.',
                                                blank=True,
                                                default=True)

    xmi_file_url = models.URLField(verbose_name='XMI source URL', blank=True, null=True, default='')

    def xmi_string(self):
        """ :return  (xmi_string, is_ok, error_message)"""
        try:

            if self.use_uploaded_xmi_file:
                if self.xmi_file.size < 10:
                    raise Exception('The .XMI file seems to be empty.')
                if self.xmi_file.size > 1000000:
                    raise Exception('The file is to large to be a Tango .XMI file.')

                xmi_string = self.xmi_file.read()

            elif self.use_url_xmi_file:
                response = urllib2.urlopen(xmi_url)
                xmi_size = response.get('Content-Length', 0)
                if xmi_size < 10:
                    raise forms.ValidationError('The .XMI file pointed by the url seems to be empty.')
                if xmi_size > 200000:
                    raise forms.ValidationError('The .XMI file pointed by the url is to large to be a Tango .XMI file.')

                xmi_string = response.read()

            parser = TangoXmiParser(xml_string=xmi_string)

            is_valid, message = parser.is_valid()

            if not is_valid:
                raise Exception(message)

        except Exception as e:
            return '', False, e.message

        return xmi_string, True, ''

    # manual info
    use_manual_info = models.BooleanField(verbose_name='Provide data manually', blank=True, default=False)
    class_name = models.CharField(max_length=64, verbose_name='Class name', blank=True, default='')
    class_description = models.TextField(verbose_name='Class description', blank=True, default='')
    contact_email = models.EmailField(verbose_name='Contact email', blank=True,default='')

    class_copyright = models.CharField(max_length=128, verbose_name="Copyright", default='', blank=True)
    language = models.CharField(max_length=32,
                                choices=zip(['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView'],
                                            ['Cpp', 'Python', 'PythonHL', 'Java', 'CSharp', 'LabView']),
                                verbose_name='Language', default='Cpp')

    class_family = models.CharField(max_length=64, blank=True, null=True, default='')  # TODO: implement choices
    platform = models.CharField(max_length=64,
                                choices=zip(['Windows', 'Unix Like', 'All Platforms'],
                                            ['Windows', 'Unix Like', 'All Platforms']),
                                verbose_name='Platform', default='All Platforms')
    bus = models.CharField(max_length=64, verbose_name='Bus', blank=True, null=True)  # TODO: implement bus choices
    manufacturer = models.CharField(max_length=64, verbose_name='Manufacturer', default='', null=True, blank=True)
    # at the beginning there will not be any manufacturer table
    key_words = models.CharField(max_length=255, verbose_name="Key words", blank=True, null=True, default='')
    product_reference = models.CharField(max_length=64, verbose_name="Product", default='', blank=True)
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

    def from_device_server(self, device_server):
        """ Fill fields based on device_server object"""
        assert isinstance(device_server, DeviceServer)
        self.name = device_server.name
        self.description = device_server.description
        self.readme_file = device_server.readme
        self.certified = device_server.certified
        self.ds_status = device_server.status
        self.development_status = device_server.development_status

        if device_server.license is not None:
            self.license_name=device_server.license.name

        if  hasattr(device_server, 'repository'):
            assert isinstance(device_server.repository, DeviceServerRepository)
            self.repository_type = device_server.repository.repository_type
            self.repository_contact = device_server.repository.contact_email
            self.repository_url = device_server.repository.url
            self.repository_download_url = device_server.repository.download_url
            self.repository_path = device_server.repository.path_in_repository

        docs = device_server.documentation.all()
        if len(docs)>0:
            self.other_documentation1 = True
            self.documentation1_type = docs[0].documentation_type
            self.documentation1_url = docs[0].url

        if len(docs)>1:
            self.other_documentation2 = True
            self.documentation2_type = docs[1].documentation_type
            self.documentation2_url = docs[1].url

        cls = device_server.device_classes.all()

        if len(cls)>0:
            cl = cls[0]
            assert isinstance(cl, DeviceClass)
            self.class_copyright = cl.class_copyright
            self.class_description = cl.description
            self.class_name = cl.name
            self.language = cl.language
            if cl.license is not None:
                self.license_name = cl.license.name

            self.class_family = cl.info.class_family
            self.manufacturer = cl.info.manufacturer
            self.product_reference = cl.info.product_reference
            self.platform = cl.info.platform
            self.bus = cl.info.bus
            self.key_words = cl.info.key_words
            self.contact_email = cl.info.contact_email

        return self


def filtered_device_servers(family=None, manufacturer=None, product=None, bus=None, key_words=None):
    """ Provides a filtered queryset of device servers"""
    q = DeviceServer.objects.filter(invalidate_activity=None)

    if manufacturer is not None:
        q = q.filter(device_classes__info__manufacturer__icontains=manufacturer)

    if product is not None:
        q = q.filter(device_classes__info__product_reference__icontains=product)

    if family is not None:
        q = q.filter(device_classes__info__class_family__icontains=family)

    if bus is not None:
        q = q.filter(device_classes__info__bus__icontains=bus)

    if key_words is not None:
        q = q.filter(device_classes__info__key_words__icontains=key_words)

    return q.filter(invalidate_activity=None)


def search_device_servers(search_text):
    """ Provides a filtered queryset of device servers"""
    q = DeviceServer.objects.filter(invalidate_activity=None).filter(device_classes__invalidate_activity=None)

    qn = q.filter(name__icontains=search_text) | q.filter(device_classes__name__icontains=search_text)

    qd = q.filter(description__icontains=search_text) | q.filter(device_classes__description__icontains=search_text)

    qm = q.filter(device_classes__info__manufacturer__icontains=search_text)

    qp = q.filter(device_classes__info__product_reference__icontains=search_text)

    qf = q.filter(device_classes__info__class_family__icontains=search_text)

    qb = q.filter(device_classes__info__bus__icontains=search_text)

    qk = q.filter(device_classes__info__key_words__icontains=search_text)

    qall = qn | qd | qm | qp | qf | qb | qk

    return qall.filter(invalidate_activity=None).distinct()


from xmi_parser import TangoXmiParser
def create_or_update(update_object, activity, device_server=None):
    """this method creates or updates device server based on update/add object. It should be used inside atimic
    transaction to keep database consistent.
        :return (device_server, backup_device_server)
    """
    assert isinstance(update_object, DeviceServerAddModel)

    backup_device_server = None
    new_device_server = None

    # backup device server if it is update
    if device_server is not None:
        backup_device_server = device_server.make_backup(activity=activity)
        backup_device_server.save()

    # basic information about device server
    if update_object.use_uploaded_xmi_file:
        # use xmi file
        xmi_string, ok, message = update_object.xmi_string()
        if ok:
            parser = TangoXmiParser(xml_string=xmi_string)
            # device server object
            new_device_server = parser.get_device_server()

    else:
        new_device_server = DeviceServer(name='', description='')

    if update_object.certified is not None:
        new_device_server.certified = update_object.certified

    if update_object.development_status is not None:
        new_device_server.development_status = update_object.development_status

    if update_object.ds_status is not None:
        new_device_server.status = update_object.ds_status

    # if data provided manually
    if update_object.use_manual_info:

        if len(update_object.name) > 0:
            new_device_server.name = update_object.name

        if len(update_object.description) > 0:
            new_device_server.description = update_object.description

        if len(update_object.license_name) > 0:
            lic = DeviceServerLicense.objects.get_or_create(name=update_object.license_name)[0]
            new_device_server.license = lic

    # make sure license object is saved
    if new_device_server.license is not None and new_device_server.license.pk is None:
        new_device_server.license.save()

    # so, we have base inforamtion
    if device_server is None:
        device_server = new_device_server
        device_server.create_activity = activity
        device_server.created_by = activity.created_by
        device_server.status = STATUS_NEW
    else:
        device_server.name = new_device_server.name
        device_server.description = new_device_server.description
        device_server.license = new_device_server.license
        device_server.last_update_activity = activity
        device_server.development_status = new_device_server.development_status
        device_server.certified = new_device_server.certified
        device_server.status = STATUS_UPDATED

    # make sure device server has pk
    device_server.save()

    # # mark it in activity
    # activity.device_server = device_server
    # activity.device_server_backup = backup_device_server
    # activity.save()

    # check repository
    new_repository = None
    if update_object.available_in_repository or update_object.repository_contact is not None \
            or update_object.repository_download_url is not None:
        if not update_object.available_in_repository:
            update_object.repository_type = None
            update_object.repository_url = None
            update_object.repository_path = None
            update_object.repository_download_url = None
        new_repository = DeviceServerRepository(repository_type=update_object.repository_type,
                                                url=update_object.repository_url,
                                                path_in_repository=update_object.repository_path,
                                                contact_email=update_object.repository_contact,
                                                download_url=update_object.repository_download_url,
                                                )
        if backup_device_server is not None:
            # if it is update operation and repository change old repo is redirected to backup device server
            # and new_repository is marked as update
            if hasattr(device_server, 'repository'):
                assert isinstance(device_server.repository, DeviceServerRepository)
                # check also if there is a real change
                if new_repository.repository_type != device_server.repository.repository_type \
                        or new_repository.url != device_server.repository.url \
                        or new_repository.path_in_repository != device_server.repository.path_in_repository \
                        or new_repository.download_url != device_server.repository.download_url \
                        or new_repository.contact_email != device_server.repository.contact_email:
                    # for modified repository move it to backup
                    old_repo = device_server.repository
                    old_repo.device_server = backup_device_server
                    old_repo.invalidate_activity = activity
                    old_repo.save()
                    new_repository.last_update_activity = activity
                    new_repository.device_server = device_server
                    new_repository.create_activity = old_repo.create_activity

                else:
                    # no real change
                    new_repository = None
        else:
            # here, it means we are creating a new device server
            new_repository.create_activity = activity
            new_repository.device_server = device_server

    # make sure the repository is saved
    if new_repository is not None:
        new_repository.last_update_activity = activity
        new_repository.device_server = device_server

        new_repository.save()

    # check documentation
    # readme is update directly
    if update_object.upload_readme:
        device_server.readme = update_object.readme_file

    # old documentation is not invalidated automatically but added
    if update_object.other_documentation1:
        new_documentation1 = DeviceServerDocumentation(documentation_type=update_object.documentation1_type,
                                                       url=update_object.documentation1_url,
                                                       create_activity=activity,
                                                       device_server=device_server)
        new_documentation1.save()

    if update_object.other_documentation2:
        new_documentation2 = DeviceServerDocumentation(documentation_type=update_object.documentation2_type,
                                                       url=update_object.documentation2_url,
                                                       create_activity=activity,
                                                       device_server=device_server)
        new_documentation2.save()

    # get classes and interface
    if ( update_object.use_uploaded_xmi_file or update_object.use_url_xmi_file ) and parser is not None:
        # for xmi file all old device classes and relation are moved to backup and new are created from scratch
        for cl in device_server.device_classes.all():
            cl.make_invalid(activity)
            if backup_device_server is not None:
                cl.device_server = backup_device_server
            cl.save()

        # read classes from xmi file
        cls = parser.get_device_classes()
        for cl in cls:
            # save class
            assert (isinstance(cl, DeviceClass))
            cl.device_server = device_server
            cl.create_activity = activity
            if backup_device_server is not None:
                cl.last_update_activity = activity
            if cl.license is not None and cl.license.pk is None:
                cl.license.save()

            cl.save()

            # create and save class info object
            class_info = parser.get_device_class_info(cl)
            assert (isinstance(class_info, DeviceClassInfo))
            class_info.device_class = cl
            class_info.create_activity = activity
            if backup_device_server is not None:
                class_info.last_update_activity = activity

            # if manual info provided override defaults
            if update_object.use_manual_info:
                if len(update_object.contact_email) > 0:
                    class_info.contact_email = update_object.contact_email

            class_info.save()

            # create and save attributes
            attributes = parser.get_device_attributes(cl)
            for attrib in attributes:
                assert (isinstance(attrib, DeviceAttribute))
                attrib.device_class = cl
                attrib.create_activity = activity
                attrib.save()

            # create and save commands
            commands = parser.get_device_commands(cl)
            for command in commands:
                assert (isinstance(command, DeviceCommand))
                command.device_class = cl
                command.create_activity = activity
                command.save()

            # create and save pipes
            pipes = parser.get_device_pipes(cl)
            for pipe in pipes:
                assert (isinstance(pipe, DevicePipe))
                pipe.device_class = cl
                pipe.create_activity = activity
                pipe.save()

            # create and save properties
            properties = parser.get_device_properties(cl)
            for prop in properties:
                assert (isinstance(prop, DeviceProperty))
                prop.device_class = cl
                prop.create_activity = activity
                prop.save()

    elif update_object.use_manual_info:
        # for clo in device_server.device_classes.all():
        #     clo.make_invalid(activity)
        #     if backup_device_server is not None:
        #         clo.device_server = backup_device_server
        #     clo.save()

        # manual info provided
        if len(device_server.device_classes.all()) > 0:
            cl = device_server.device_classes.all()[0]
            cl.last_update_activity = activity
            cl_info = cl.info
            cl_info.last_update_activity = activity
        else:
            cl = DeviceClass()
            cl.create_activity = activity
            cl_info = DeviceClassInfo()
            cl_info.create_activity = activity

        cl.name = update_object.name
        cl.description = update_object.description
        cl.class_copyright = update_object.class_copyright
        cl.language = update_object.language
        cl.device_server = device_server

        if len(update_object.license_name) > 0:
            lic = DeviceServerLicense.objects.get_or_create(name=update_object.license_name)[0]
            if lic.pk is None:
                lic.save()
            cl.license = lic

        cl.save()

        cl_info.device_class = cl
        cl_info.contact_email = update_object.contact_email
        cl_info.class_family = update_object.class_family
        cl_info.platform = update_object.platform
        cl_info.bus = update_object.bus
        cl_info.manufacturer = update_object.manufacturer
        cl_info.product_reference = update_object.product_reference
        cl_info.key_words = update_object.key_words

        cl_info.save()

    # return device_server
    return device_server, backup_device_server


###################################################################################


class DeviceServerPluginModel(CMSPlugin):
    model = DeviceServerActivity

    # TODO prepare plugin for administration CMS
    class Meta:
        app_label = 'dsc'
        verbose_name = 'Device Servers Catalogue plugin'


class DeviceServersActivityPluginModel(CMSPlugin):
    model = DeviceServer

    items_number = models.PositiveSmallIntegerField(verbose_name="Number of items", default=5)

    # TODO prepare plugin for administration CMS
    class Meta:
        app_label = 'dsc'
        verbose_name = 'Device Servers Catalogue Activity plugin'

