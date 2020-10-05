# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('dsc', '0002_auto_20160715_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceServerPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'verbose_name': 'Device Servers Catalogue plugin',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterModelOptions(
            name='deviceserver',
            options={'ordering': ['name'], 'verbose_name': 'device server', 'verbose_name_plural': 'device servers'},
        ),
        migrations.AddField(
            model_name='deviceserver',
            name='status',
            field=models.CharField(default=b'new', max_length=10, verbose_name=b'Status', choices=[(b'new', b'New'), (b'updated', b'Updated'), (b'certified', b'Certified'), (b'archived', b'Archived'), (b'deleted', b'Deleted')]),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='license',
            field=models.ForeignKey(related_name='licensed_device_servers', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'License', blank=True, to='dsc.DeviceServerLicense', null=True),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'Device Server'),
        ),
        migrations.AlterField(
            model_name='deviceserveractivity',
            name='activity_type',
            field=models.CharField(max_length=10, verbose_name=b'Activity', choices=[(b'add', b'Add'), (b'edit', b'Edit'), (b'download', b'Download'), (b'delete', b'Delete'), (b'apply_for_cert', b'Apply for cerification'), (b'certify', b'Certify')]),
        ),
        migrations.AlterField(
            model_name='deviceserveractivity',
            name='created_by',
            field=models.ForeignKey(related_name='device_servers_activities', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='repository_type',
            field=models.SlugField(verbose_name=b'Repository'),
        ),
    ]
