# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0009_auto_20161105_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserver',
            name='add_device_object',
            field=models.ForeignKey(related_name='device_server_created', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Created with', blank=True, to='dsc.DeviceServerAddModel', null=True),
        ),
    ]
