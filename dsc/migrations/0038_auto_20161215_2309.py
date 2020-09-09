# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0037_auto_20161214_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceclass',
            name='class_copyright',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Copyright', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='bus',
            field=models.CharField(max_length=128, null=True, verbose_name=b'Bus', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='class_copyright',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Copyright', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='manufacturer',
            field=models.CharField(default=b'', max_length=128, null=True, verbose_name=b'Manufacturer', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='product_reference',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Product', blank=True),
        ),
    ]
