# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0049_auto_20170804_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceClassFamily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('family', models.CharField(default=b'', max_length=128, unique=True, null=True, blank=True)),
                ('create_activity', models.ForeignKey(related_name='created_deviceclassfamily', default=None, blank=True, to='dsc.DeviceServerActivity', null=True)),
                ('device_class', models.ManyToManyField(related_name='additional_families', to='dsc.DeviceClassInfo')),
                ('invalidate_activity', models.ForeignKey(related_name='invalidated_deviceclassfamily', default=None, blank=True, to='dsc.DeviceServerActivity', null=True)),
                ('last_update_activity', models.ForeignKey(related_name='updated_deviceclassfamily', default=None, blank=True, to='dsc.DeviceServerActivity', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
