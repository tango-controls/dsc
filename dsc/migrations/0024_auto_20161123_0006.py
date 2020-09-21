# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('dsc', '0023_auto_20161122_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceServersActivityPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('items_number', models.PositiveSmallIntegerField(default=5, verbose_name=b'Number of items')),
            ],
            options={
                'verbose_name': 'Device Servers Catalogue Activity plugin',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='deviceattribute',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceattribute', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceattribute',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceattribute', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceattribute',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceattribute', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceattributeinfo',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceattributeinfo', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceattributeinfo',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceattributeinfo', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceattributeinfo',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceattributeinfo', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceclass',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceclass', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceclass',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceclass', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceclass',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceclass', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceclassinfo', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceclassinfo', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceclassinfo', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='create_activity',
            field=models.ForeignKey(related_name='created_devicecommand', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_devicecommand', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_devicecommand', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='devicepipe',
            name='create_activity',
            field=models.ForeignKey(related_name='created_devicepipe', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='devicepipe',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_devicepipe', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='devicepipe',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_devicepipe', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceproperty',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceproperty', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceproperty',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceproperty', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceproperty',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceproperty', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceserver', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceserver', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceserver', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserverdocumentation',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceserverdocumentation', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserverdocumentation',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceserverdocumentation', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserverdocumentation',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceserverdocumentation', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceserverrepository', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceserverrepository', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceserverrepository', default=None, blank=True, to='dsc.DeviceServerActivity', null=True),
        ),
    ]
