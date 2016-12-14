import django_tables2 as tables
from models import DeviceServer, DeviceServerActivity, DeviceAttribute, DeviceProperty, DevicePipe, DeviceCommand
from django_tables2.utils import A

class DeviceServerTable(tables.Table):

    name = tables.LinkColumn('deviceserver_detail', args=[A('pk')] )

    manufacturers = tables.Column(accessor='device_classes', verbose_name='Manufacturer',
                                  order_by='device_classes__info__manufacturer')

    def render_manufacturers(self, value, table):
        rednered_value = ""
        vFirst = True
        vList = list(value.filter(invalidate_activity=None))
        for u in vList:
            if not vFirst:
                rednered_value += ", "
            else:
                vFirst = False
            rednered_value += u.info.manufacturer
        return rednered_value


    products = tables.Column(accessor='device_classes', verbose_name='Products',
                             order_by="device_classes__info__product_reference")

    def render_products(self, value, table):
        rednered_value = ""
        vFirst = True
        vList = list(value.filter(invalidate_activity=None))
        for u in vList:
            if not vFirst:
                rednered_value += ", "
            else:
                vFirst = False
            rednered_value += u.info.product_reference
        return rednered_value


    family = tables.Column(accessor='device_classes', verbose_name='Family',
                           order_by="device_classes__info__class_family")

    def render_family(self, value, table):
        rednered_value = ""
        vFirst = True
        vList = list(value.filter(invalidate_activity=None))
        for u in vList:
            if not vFirst:
                rednered_value += ", "
            else:
                vFirst = False
            rednered_value += u.info.class_family
        return rednered_value

    class Meta:
        model = DeviceServer
        fields = ('name',)
        sequence = ('name', 'family', 'manufacturers', 'products')


class DeviceServerSearchTable(DeviceServerTable):

    class Meta:
        model = DeviceServer
        fields = ('name', 'family', 'manufacturers', 'products')
        sequence = ('name', 'family', 'manufacturers', 'products')
        exclude = ('license',)


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