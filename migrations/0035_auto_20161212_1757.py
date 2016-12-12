# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0034_auto_20161212_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceclass',
            name='name',
            field=models.CharField(max_length=128, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='bus',
            field=models.CharField(max_length=128, null=True, verbose_name=b'Bus', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='class_family',
            field=models.CharField(default=b'', max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='manufacturer',
            field=models.CharField(default=b'', max_length=128, null=True, verbose_name=b'Manufacturer'),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='product_reference',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Product'),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='development_status',
            field=models.CharField(default=b'new', max_length=20, verbose_name=b'Development status', blank=True, choices=[(b'new', b'New development'), (b'released', b'Released'), (b'maintenance', b'In maintenance'), (b'broken', b'Broken')]),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='name',
            field=models.CharField(max_length=128, verbose_name=b'Device Server'),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='status',
            field=models.CharField(default=b'new', max_length=20, verbose_name=b'Information status', choices=[(b'new', b'New'), (b'verified', b'Verified'), (b'updated', b'Updated'), (b'certified', b'Certified'), (b'archived', b'Archived'), (b'deleted', b'Deleted')]),
        ),
    ]
