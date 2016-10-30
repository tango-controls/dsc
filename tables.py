import django_tables2 as tables
from models import DeviceServer, DeviceServerActivity, DeviceAttribute, DeviceProperty, DevicePipe, DeviceCommand
from django_tables2.utils import A

class DeviceServerTable(tables.Table):
    repository = tables.Column(accessor='repository.path_in_repository')
    #TODO add activitytype = download and here should be the sum
    downloads = tables.Column(accessor='activities.activity_type', verbose_name= 'Downloads')
    #TODO NO category in the model - must be add
    name = tables.LinkColumn('deviceserver_detail', args=[A('pk')] )
    selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input":
                                        {"onclick": "toggle(this)"}},
                                         orderable=False)

    class Meta:
        model = DeviceServer
        fields = ('name', 'repository', 'license')
        sequence = ('selection', 'name','repository', 'license', 'downloads',)


class DevicePropertiesTable(tables.Table):
    class Meta:
        model = DeviceProperty
        fields = ('name','property_type', 'description')


class DeviceAttributesTable(tables.Table):
    class Meta:
        model = DeviceAttribute
        fields = ('name','attribute_type', 'description')


class DevicePipesTable(tables.Table):
    class Meta:
        model = DevicePipe
        fields = ('name', 'description')


class DeviceCommandsTable(tables.Table):
    class Meta:
        model = DeviceCommand
        fields = ('name','description')