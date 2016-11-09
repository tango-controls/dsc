# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0014_auto_20161107_2343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceserver',
            options={'permissions': (('admin_deviceserver', 'do various administration tasks on device servers'),)},
        ),
    ]
