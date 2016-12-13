# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0035_auto_20161212_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='ds_info_copy',
            field=models.BooleanField(default=True, verbose_name=b'Guess device server name and description from class info?'),
        ),
    ]
