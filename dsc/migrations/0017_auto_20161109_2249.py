# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0016_auto_20161109_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceserver',
            options={'permissions': (('admin_deviceserver', 'do various administration tasks on device servers'), ('update_own_deviceserver', 'do changes to device server for creator'), ('delete_own_deviceserver', 'deletion of device server for creator'))},
        ),
    ]
