# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('attribute_type', models.SlugField()),
                ('data_type', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceAttributeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_attribute', models.OneToOneField(related_name='attribute_info', to='dsc.DeviceAttribute')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceClassInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('xmi_file', models.CharField(max_length=128)),
                ('contact_email', models.EmailField(max_length=254)),
                ('class_family', models.CharField(max_length=64)),
                ('platform', models.CharField(max_length=64)),
                ('bus', models.CharField(max_length=64)),
                ('manufacturer', models.CharField(max_length=64)),
                ('key_words', models.SlugField()),
                ('device_class', models.OneToOneField(related_name='info', to='dsc.DeviceClass')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceCommand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('input_type', models.SlugField()),
                ('output_type', models.SlugField()),
                ('device_class', models.ForeignKey(related_name='commands', to='dsc.DeviceClass')),
            ],
        ),
        migrations.CreateModel(
            name='DevicePipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('device_class', models.ForeignKey(related_name='pipes', to='dsc.DeviceClass')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('property_type', models.SlugField()),
                ('device_class', models.ForeignKey(related_name='properties', to='dsc.DeviceClass')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='created_device_servers', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceServerActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.SlugField()),
                ('activity_info', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='device_servers_cativities', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('device_server', models.ForeignKey(related_name='activities', to='dsc.DeviceServer')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceServerDocumentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documentation_type', models.SlugField()),
                ('url', models.URLField()),
                ('device_server', models.ForeignKey(related_name='documentation', to='dsc.DeviceServer')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceServerLicnese',
            fields=[
                ('name', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('description', models.TextField()),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceServerRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('repository_type', models.SlugField()),
                ('url', models.URLField()),
                ('path_in_repository', models.CharField(max_length=255)),
                ('device_server', models.OneToOneField(related_name='repository', to='dsc.DeviceServer')),
            ],
        ),
        migrations.AddField(
            model_name='deviceserver',
            name='license',
            field=models.ForeignKey(related_name='licensed_device_servers', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dsc.DeviceServerLicnese', null=True),
        ),
        migrations.AddField(
            model_name='deviceclass',
            name='device_server',
            field=models.ForeignKey(related_name='device_classes', to='dsc.DeviceServer'),
        ),
        migrations.AddField(
            model_name='deviceattribute',
            name='device_class',
            field=models.ForeignKey(related_name='attributes', to='dsc.DeviceClass'),
        ),
    ]
