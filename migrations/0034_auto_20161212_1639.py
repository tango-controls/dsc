# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0033_auto_20161212_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='language',
            field=models.CharField(default=b'Cpp', max_length=32, verbose_name=b'Language', blank=True, choices=[(b'Cpp', b'Cpp'), (b'Python', b'Python'), (b'PythonHL', b'PythonHL'), (b'Java', b'Java'), (b'CSharp', b'CSharp'), (b'LabView', b'LabView')]),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='platform',
            field=models.CharField(default=b'All Platforms', max_length=64, verbose_name=b'Platform', blank=True, choices=[(b'Windows', b'Windows'), (b'Unix Like', b'Unix Like'), (b'All Platforms', b'All Platforms')]),
        ),
    ]
