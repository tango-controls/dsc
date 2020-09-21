# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0060_auto_20171219_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserverupdatemodel',
            name='only_github',
            field=models.BooleanField(default=False, verbose_name=b'Updated only github?'),
        ),
    ]
