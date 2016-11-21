# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0021_auto_20161120_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserverrepository',
            name='download_url',
            field=models.URLField(null=True, verbose_name=b'Download URL'),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='url',
            field=models.URLField(null=True, verbose_name=b'URL'),
        ),
    ]
