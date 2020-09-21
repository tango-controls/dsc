# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0012_auto_20161106_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='xmi_file',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='readme',
            field=models.FileField(max_length=100000, upload_to=b'dsc_readmes', null=True, verbose_name=b'Readme', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='contact_email',
            field=models.EmailField(default=b'', max_length=254, verbose_name=b'Contact email', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='readme_file',
            field=models.FileField(max_length=100000, upload_to=b'dsc_readmes', null=True, verbose_name=b'README file', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='repository_path',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Path within reposiroty', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='repository_url',
            field=models.URLField(default=b'', verbose_name=b'Repository URL', blank=True),
        ),
    ]
