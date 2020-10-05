# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0054_families_admin_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='additional_families',
            field=models.ManyToManyField(related_name='device_class_infos', to='dsc.DeviceClassFamily', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='additional_families',
            field=models.ManyToManyField(to='dsc.DeviceClassFamily', blank=True),
        ),
    ]
