# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dsc', '0006_auto_20161031_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceServerAddModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'Name')),
                ('description', models.TextField(verbose_name=b'Description', blank=True)),
                ('process_from_repository', models.BooleanField(default=False, verbose_name=b'Use repository only')),
                ('repository_type', models.SlugField(verbose_name=b'Repository Type', choices=[(b'GIT', b'GIT'), (b'SVN', b'SVN'), (b'Mercurial', b'Mercurial'), (b'FTP', b'FTP'), (b'Other', b'Other')])),
                ('repository_url', models.URLField(verbose_name=b'URL')),
                ('repository_path', models.CharField(default=b'', max_length=255, verbose_name=b'Path', blank=True)),
                ('readme_file', models.FileField(upload_to=b'dsc_readmes', null=True, verbose_name=b'README upload file:', blank=True)),
                ('documentation1_type', models.SlugField(choices=[(b'README', b'README'), (b'Manual', b'Manual'), (b'InstGuide', b'Installation Guide'), (b'Generated', b'Generated'), (b'SourceDoc', b'Source Documentation')], blank=True, null=True, verbose_name=b'Documentation type')),
                ('documentation1_url', models.URLField(default=b'', null=True, verbose_name=b'URL', blank=True)),
                ('documentation2_type', models.SlugField(choices=[(b'README', b'README'), (b'Manual', b'Manual'), (b'InstGuide', b'Installation Guide'), (b'Generated', b'Generated'), (b'SourceDoc', b'Source Documentation')], blank=True, null=True, verbose_name=b'Documentation type')),
                ('documentation2_url', models.URLField(default=b'', null=True, verbose_name=b'URL', blank=True)),
                ('use_uploaded_xmi_file', models.BooleanField(default=True, verbose_name=b'Use uploaded .xmi to populate database')),
                ('xmi_file', models.FileField(upload_to=b'dsc_xmi_files', null=True, verbose_name=b'DeviceServer XMI file', blank=True)),
                ('use_manual_info', models.BooleanField(default=False, verbose_name=b'Provide all data manualy')),
                ('class_name', models.CharField(max_length=64, verbose_name=b'Name', blank=True)),
                ('contact_email', models.EmailField(max_length=254, verbose_name=b'Contact')),
                ('class_copyright', models.CharField(default=b'', max_length=128, verbose_name=b'Copyright', blank=True)),
                ('language', models.CharField(default=b'Cpp', max_length=32, verbose_name=b'Language', choices=[(b'Cpp', b'Cpp'), (b'Python', b'Python'), (b'PythonHL', b'PythonHL'), (b'Java', b'Java'), (b'CSharp', b'CSharp'), (b'LabView', b'LabView')])),
                ('class_family', models.CharField(default=b'', max_length=64, null=True, blank=True)),
                ('platform', models.CharField(default=b'All Platforms', max_length=64, verbose_name=b'Platform', choices=[(b'Windows', b'Windows'), (b'Unix Like', b'Unix Like'), (b'All Platforms', b'All Platforms')])),
                ('bus', models.CharField(max_length=64, null=True, verbose_name=b'Bus', blank=True)),
                ('manufacturer', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Manufacturer', blank=True)),
                ('key_words', models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Key words', blank=True)),
                ('product_reference', models.CharField(default=b'', max_length=64, verbose_name=b'Product')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed_ok', models.BooleanField(default=False)),
                ('processed_with_errors', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='device_servers_add_activities', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
