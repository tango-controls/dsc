# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0018_auto_20161109_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceserver',
            name='add_device_object',
        ),
        migrations.AddField(
            model_name='deviceattribute',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceattribute', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceattribute',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceattribute', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceattribute',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceattribute', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceattributeinfo',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceattributeinfo', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceattributeinfo',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceattributeinfo', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceattributeinfo',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceattributeinfo', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceclass',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceclass', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceclass',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceclass', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceclass',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceclass', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceclassinfo',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceclassinfo', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceclassinfo',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceclassinfo', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceclassinfo',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceclassinfo', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='devicecommand',
            name='create_activity',
            field=models.ForeignKey(related_name='created_devicecommand', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='devicecommand',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_devicecommand', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='devicecommand',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_devicecommand', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='devicepipe',
            name='create_activity',
            field=models.ForeignKey(related_name='created_devicepipe', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='devicepipe',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_devicepipe', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='devicepipe',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_devicepipe', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceproperty',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceproperty', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceproperty',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceproperty', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceproperty',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceproperty', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserver',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceserver', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserver',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceserver', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserver',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceserver', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserveractivity',
            name='device_server_backup',
            field=models.ForeignKey(related_name='backup_for', blank=True, to='dsc.DeviceServer', null=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='activity',
            field=models.ForeignKey(related_name='create_object', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='repository_contact',
            field=models.EmailField(default=b'', max_length=254, null=True, verbose_name=b'Please write to', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='repository_download_url',
            field=models.URLField(default=b'', verbose_name=b'Dwonload URL', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserverdocumentation',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceserverdocumentation', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserverdocumentation',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceserverdocumentation', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserverdocumentation',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceserverdocumentation', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserverrepository',
            name='contact_email',
            field=models.EmailField(default=b'', max_length=254, null=True, verbose_name=b'Please write to', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserverrepository',
            name='create_activity',
            field=models.ForeignKey(related_name='created_deviceserverrepository', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserverrepository',
            name='invalidate_activity',
            field=models.ForeignKey(related_name='invalidated_deviceserverrepository', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AddField(
            model_name='deviceserverrepository',
            name='last_update_activity',
            field=models.ForeignKey(related_name='updated_deviceserverrepository', default=None, to='dsc.DeviceServerActivity', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserveractivity',
            name='activity_type',
            field=models.CharField(max_length=10, verbose_name=b'Activity', choices=[(b'add', b'Create'), (b'edit', b'Update'), (b'download', b'Download'), (b'delete', b'Delete'), (b'apply_for_cert', b'Apply for certification'), (b'certify', b'Certificate'), (b'verify', b'Verify'), (b'verify', b'Revert')]),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='device_server',
            field=models.OneToOneField(related_name='repository', null=True, to='dsc.DeviceServer'),
        ),
    ]
