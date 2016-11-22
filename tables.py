import django_tables2 as tables
from models import DeviceServer, DeviceServerActivity, DeviceAttribute, DeviceProperty, DevicePipe, DeviceCommand
from django_tables2.utils import A

class DeviceServerTable(tables.Table):
    # repository = tables.Column(accessor='repository.url', verbose_name='Repository')
    # TODO add activitytype = download and here should be the sum
    # downloads = tables.Column(accessor='activities.activity_type', verbose_name= 'Downloads')
    # TODO NO category in the model - must be add
    name = tables.LinkColumn('deviceserver_detail', args=[A('pk')] )
    # selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input":
    #                                    {"onclick": "toggle(this)"}},
    #                                     orderable=False)
    manufacturers = tables.Column(accessor='manufacturers', verbose_name='Manufacturer', orderable=False)
    products = tables.Column(accessor='products', verbose_name='Products',
                             orderable=False)
    family = tables.Column(accessor='family', verbose_name='Family',
                           orderable=False)

    class Meta:
        model = DeviceServer
        fields = ('name', 'license')
        sequence = ('name', 'license','family', 'manufacturers', 'products')


class DeviceServerSearchTable(tables.Table):

    name = tables.LinkColumn('deviceserver_detail', args=[A('pk')] )
    manufacturers = tables.Column(accessor='manufacturers', verbose_name='Manufacturer', orderable=False)
    products = tables.Column(accessor='products', verbose_name='Products',
                             orderable=False)
    family = tables.Column(accessor='family', verbose_name='Family',
                           orderable=False)

    class Meta:
        model = DeviceServer
        fields = ('name',)
        sequence = ('name', 'family', 'manufacturers', 'products')


class DevicePropertiesTable(tables.Table):
    class Meta:
        model = DeviceProperty
        fields = ('name', 'description')


class DeviceAttributesTable(tables.Table):
    class Meta:
        model = DeviceAttribute
        fields = ('name','description')


class DevicePipesTable(tables.Table):
    class Meta:
        model = DevicePipe
        fields = ('name', 'description')


class DeviceCommandsTable(tables.Table):
    class Meta:
        model = DeviceCommand
        fields = ('name','description')


class DeviceServerActivityTable(tables.Table):
    class Meta:
        model = DeviceServerActivity
        fields = ('activity_type', 'activity_info')