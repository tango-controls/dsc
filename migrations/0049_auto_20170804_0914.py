# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0048_auto_20170128_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserver',
            name='picture',
            field=models.ImageField(max_length=1048576, upload_to=b'dsc_pictures', null=True, verbose_name=b'Picture', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='picture',
            field=models.ImageField(max_length=1048576, upload_to=b'dsc_pictures', null=True, verbose_name=b'Picture', blank=True),
        ),
    ]
