import django_tables2 as tables
from models import DeviceServer, DeviceServerActivity, DeviceAttribute, DeviceProperty, DevicePipe, DeviceCommand, \
    DS_COMMAND_DATATYPES, DS_ATTRIBUTE_DATATYPES, DS_PROPERTIES_DATATYPES
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
            if u.info.manufacturer is not None:
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
            if u.info.product_reference is not None:
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
            if u.info.class_family is not None:
                rednered_value += u.info.class_family
        return rednered_value

    class Meta:
        model = DeviceServer
        fields = ('name',)
        sequence = ('name', 'family', 'manufacturers', 'products')
        template = 'dsc/inc/ds_table.html'


class DeviceServerSearchTable(DeviceServerTable):

    class Meta:
        model = DeviceServer
        fields = ('name', 'family', 'manufacturers', 'products')
        sequence = ('name', 'family', 'manufacturers', 'products')
        exclude = ('license',)
        template = 'dsc/inc/ds_table.html'


class DSCTooltipTable(tables.Table):

    def tooltip_style(self, record):
        # return 'style="width:%dpx;"' % (10*min(40, len(str(self.tooltip(record)).strip())))
        return 'style="width: -webkit-min-content;  width: -moz-min-content; width:min-content;"'

    def tooltip(self, record):
        return record.pk

    def tooltip_class(self, record):
        return 'dsc-tooltip'

    def render_name(self, record, value):
        return mark_safe('<span class="'+self.tooltip_class(record)+'">'+str(value)+'<span class="tooltiptext "'+\
                         self.tooltip_style(record) + ' >' + str(self.tooltip(record)) + "</span></span>")


class DevicePropertiesTable(DSCTooltipTable):

    def tooltip(self, record):
        if DS_PROPERTIES_DATATYPES.has_key(str(record.property_type)):
            return DS_PROPERTIES_DATATYPES.get(str(record.property_type))
        return record.property_type

    class Meta:
        model = DeviceProperty
        fields = ('name', 'description')


class DeviceAttributesTable(DSCTooltipTable):

    # def tooltip_style(self, record):
    #    return 'style="width:%dem;"' % (min(40, len(str(self.tooltip(record)))-36))

    def tooltip(self, record):
        # workaround for missed data types
        try:
            if 'Type' in str(record.data_type) and DS_ATTRIBUTE_DATATYPES.has_key(str(record.data_type).split(':')[1]):
                record.data_type = DS_ATTRIBUTE_DATATYPES.get(str(record.data_type).split(':')[1])
        except Exception:
            pass

        return '<span style="font-weight:bold;">' + str(record.attribute_type) + '</span>:&nbsp;'+str(record.data_type)

    class Meta:
        model = DeviceAttribute
        fields = ('name','description')


class DevicePipesTable(tables.Table):
    class Meta:
        model = DevicePipe
        fields = ('name', 'description')


class DeviceCommandsTable(DSCTooltipTable):

    #def tooltip_style(self, record):
    #    return 'style="width:%dem;"' % (1*max(15, len(str(record.input_description)),
    #                                           len(str(record.output_description))))

    def tooltip(self, record):
        # workaround for missed data types
        try:
            if 'Type' in str(record.input_type) and DS_COMMAND_DATATYPES.has_key(str(record.input_type).split(':')[1]):
                record.input_type = DS_COMMAND_DATATYPES.get(str(record.input_type).split(':')[1])
        except:
            pass

        try:
            if 'Type' in str(record.output_type) and DS_COMMAND_DATATYPES.has_key(str(record.output_type).split(':')[1]):
                record.output_type = DS_COMMAND_DATATYPES.get(str(record.output_type).split(':')[1])
        except:
            pass

        ret = '<span style="font-weight:bold;">Input:</span>&nbsp;'+ str(record.input_type)
        if str(record.input_description).lower() not in ['none', '', 'null', 'nil', 'n/a', 'none.']:
            ret += '<br /><span style="text-align:left;">%s</span>' % str(record.input_description)
        ret += '<br /><span style="font-weight:bold;">Output:</span>&nbsp;' + str(record.output_type)
        if str(record.output_description).lower() not in ['none', '', 'null', 'nil', 'n/a', 'none.']:
            ret += '<br /><span style="text-align:left;">%s</span>' % str(record.output_description)

        return ret

    class Meta:
        model = DeviceCommand
        fields = ('name','description')


class DeviceServerActivityTable(tables.Table):
    class Meta:
        model = DeviceServerActivity
        fields = ('activity_type', 'activity_info')