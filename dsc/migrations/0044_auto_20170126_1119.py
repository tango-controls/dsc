# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0043_auto_20170117_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserverupdatemodel',
            name='change_update_method',
            field=models.BooleanField(default=False, verbose_name=b'Change update method'),
        ),
        migrations.AddField(
            model_name='deviceserverupdatemodel',
            name='last_update_method',
            field=models.CharField(default=b'url', max_length=32, verbose_name=b'Previous update method: ', blank=True, choices=[(b'manual', b'manual'), (b'file', b'file'), (b'url', b'url')]),
        ),
    ]
