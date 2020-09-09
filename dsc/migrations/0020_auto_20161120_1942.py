# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0019_auto_20161120_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserveractivity',
            name='device_server',
            field=models.ForeignKey(related_name='activities', blank=True, to='dsc.DeviceServer', null=True),
        ),
    ]
