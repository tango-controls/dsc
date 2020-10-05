# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0011_auto_20161106_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserver',
            name='readme',
            field=models.FileField(upload_to=b'dsc_readmes', null=True, verbose_name=b'Readme', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='class_description',
            field=models.TextField(default=b'', verbose_name=b'Class description', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='license_name',
            field=models.CharField(default=b'GPL', max_length=64, verbose_name=b'License type', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='other_documentation1',
            field=models.BooleanField(default=False, verbose_name=b'Link to other documentation'),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='other_documentation2',
            field=models.BooleanField(default=False, verbose_name=b'Link to other documentation'),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='upload_readme',
            field=models.BooleanField(default=False, verbose_name=b'Upload README'),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='class_name',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'Class name', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='name',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'Device server name', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='readme_file',
            field=models.FileField(upload_to=b'dsc_readmes', null=True, verbose_name=b'README file', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='use_uploaded_xmi_file',
            field=models.BooleanField(default=True, verbose_name=b'Upload .xmi file to populate database.'),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='xmi_file',
            field=models.FileField(upload_to=b'dsc_xmi_files', null=True, verbose_name=b'.XMI file', blank=True),
        ),
    ]
