# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0050_deviceclassfamily'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceclassfamily',
            name='device_class',
        ),
        migrations.AddField(
            model_name='deviceclassinfo',
            name='additional_families',
            field=models.ManyToManyField(related_name='device_class_infos', to='dsc.DeviceClassFamily'),
        ),
        migrations.AlterField(
            model_name='deviceclassfamily',
            name='family',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
