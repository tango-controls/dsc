# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0045_auto_20170127_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation1_file',
            field=models.FileField(max_length=2000000, upload_to=b'dsc_readmes', null=True, verbose_name=b'Document', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation1_title',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Title', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation2_file',
            field=models.FileField(max_length=2000000, upload_to=b'dsc_readmes', null=True, verbose_name=b'Document', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation2_title',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Title', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='script_operation',
            field=models.BooleanField(default=False, verbose_name=b'Updated with script?'),
        ),
    ]
