import django_tables2 as tables
from models import DeviceServer, DeviceServerActivity, DeviceAttribute, DeviceProperty, DevicePipe, DeviceCommand
from django_tables2.utils import A
from django.utils.safestring import mark_safe

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


class DSCTooltipTable(tables.Table):

    def tooltip(self, record):
        return record.pk

    def render_name(self, record, value):
        return mark_safe('<span class="dsc-tooltip">'+str(value)+'<span class="tooltiptext">'+str(self.tooltip(record))\
               +"</span></span>")

class DevicePropertiesTable(DSCTooltipTable):

    def tooltip(self, record):
        return record.property_type

    class Meta:
        model = DeviceProperty
        fields = ('name', 'description')


class DeviceAttributesTable(DSCTooltipTable):

    def tooltip(self, record):
        return str(record.attribute_type )+ ': '+str(record.data_type)

    class Meta:
        model = DeviceAttribute
        fields = ('name','description')


class DevicePipesTable(tables.Table):
    class Meta:
        model = DevicePipe
        fields = ('name', 'description')


class DeviceCommandsTable(DSCTooltipTable):

    def tooltip(self, record):

        return 'ArgIn: '+ str(record.input_type) + ', ' + str(record.input_description) + \
               '<br />ArgOut: ' + str(record.output_type) + ', ' + str(record.output_description)

    class Meta:
        model = DeviceCommand
        fields = ('name','description')


class DeviceServerActivityTable(tables.Table):
    class Meta:
        model = DeviceServerActivity
        fields = ('activity_type', 'activity_info')