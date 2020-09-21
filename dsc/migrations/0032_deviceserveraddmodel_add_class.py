# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0031_auto_20161212_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='add_class',
            field=models.BooleanField(default=False, verbose_name=b'Add new class to the device server instead of updating existing ones.'),
        ),
    ]
