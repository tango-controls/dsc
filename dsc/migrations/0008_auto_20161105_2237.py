# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0007_deviceserveraddmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='available_in_repository',
            field=models.BooleanField(default=False, verbose_name=b'Available in repository'),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='class_name',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'Name', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='contact_email',
            field=models.EmailField(default=b'', max_length=254, verbose_name=b'Contact', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='description',
            field=models.TextField(default=b'', verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='name',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'Name', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='product_reference',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'Product', blank=True),
        ),
    ]
