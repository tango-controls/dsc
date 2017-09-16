# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0051_auto_20170824_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='additional_families',
            field=models.ManyToManyField(to='dsc.DeviceClassFamily'),
        ),
    ]
