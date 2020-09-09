# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0027_auto_20161207_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='download_url',
            field=models.URLField(null=True, verbose_name=b'Download URL', blank=True),
        ),
    ]
