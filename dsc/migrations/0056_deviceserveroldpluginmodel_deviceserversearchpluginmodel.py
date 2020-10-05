# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('dsc', '0055_auto_20170925_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceServerOldPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'verbose_name': 'Device Classes Catalogue Old plugin',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='DeviceServerSearchPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'verbose_name': 'Device Classes Catalogue Search plugin',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
