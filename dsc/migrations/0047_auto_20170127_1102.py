# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0046_auto_20170127_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation3_file',
            field=models.FileField(max_length=2000000, upload_to=b'dsc_readmes', null=True, verbose_name=b'Document', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation3_title',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Title', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation3_type',
            field=models.SlugField(choices=[(b'README', b'README'), (b'Manual', b'Manual'), (b'InstGuide', b'Installation Guide'), (b'Generated', b'Generated'), (b'SourceDoc', b'Source Documentation')], blank=True, null=True, verbose_name=b'Documentation type'),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation3_url',
            field=models.URLField(default=b'', null=True, verbose_name=b'URL', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='other_documentation3',
            field=models.BooleanField(default=False, verbose_name=b'Other documentation - 3'),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='other_documentation1',
            field=models.BooleanField(default=False, verbose_name=b'Other documentation - 1'),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='other_documentation2',
            field=models.BooleanField(default=False, verbose_name=b'Other documentation - 2'),
        ),
    ]
