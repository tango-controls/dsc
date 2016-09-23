import django_tables2 as tables
from models import DeviceServer, DeviceServerActivity
from django_tables2.utils import A

class DeviceServerTable(tables.Table):
    #repository = tables.Column(accessor='repository.path_in_repository')
    #TODO add activitytype = download and here should be the sum
    #downloads = tables.Column(accessor='activities.activity_type', verbose_name= 'Downloads')
    #TODO NO category in the model - must be add
    #name = tables.LinkColumn() #'deviceserver_detail', args=[A('pk')], empty_values=()
    #selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input":
    #                                    {"onclick": "toggle(this)"}},
    #                                     orderable=False)

    class Meta:
        model = DeviceServer
        fields = ('name',)
        # sequence = ('selection', 'name',) #'repository', 'license', 'downloads',)

