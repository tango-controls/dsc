# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0042_auto_20170117_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='development_status',
            field=models.CharField(default=b'new', max_length=20, verbose_name=b'Development status', blank=True, choices=[(b'new', b'New development'), (b'released', b'Released'), (b'maintenance', b'In maintenance'), (b'broken', b'Broken')]),
        ),
    ]
