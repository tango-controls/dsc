# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0040_auto_20170116_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='repository_tag',
            field=models.CharField(default=b'', max_length=128, null=True, verbose_name=b'Tag', blank=True),
        ),
    ]
