# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0029_auto_20161207_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='use_url_xmi_file',
            field=models.BooleanField(default=True, verbose_name=b'Provide .xmi file URL populate database.'),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='xmi_file_url',
            field=models.URLField(default=b'', null=True, verbose_name=b'XMI source URL', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserverrepository',
            name='tag',
            field=models.CharField(default=b'', max_length=128, null=True, verbose_name=b'Tag', blank=True),
        ),
    ]
