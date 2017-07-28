# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0028_auto_20161207_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserver',
            name='certified',
            field=models.BooleanField(default=False, verbose_name=b'Certified'),
        ),
        migrations.AddField(
            model_name='deviceserver',
            name='development_status',
            field=models.CharField(default=b'new', max_length=10, verbose_name=b'Development status', blank=True, choices=[(b'new', b'New development'), (b'released', b'Released'), (b'maintenance', b'In maintenance'), (b'broken', b'Broken')]),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='certified',
            field=models.BooleanField(default=False, verbose_name=b'Certified'),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='development_status',
            field=models.CharField(default=b'new', max_length=10, verbose_name=b'Development status', blank=True, choices=[(b'new', b'New development'), (b'released', b'Released'), (b'maintenance', b'In maintenance'), (b'broken', b'Broken')]),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='ds_status',
            field=models.CharField(default=b'new', max_length=10, verbose_name=b'Information status', choices=[(b'new', b'New'), (b'verified', b'Verified'), (b'updated', b'Updated'), (b'certified', b'Certified'), (b'archived', b'Archived'), (b'deleted', b'Deleted')]),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='status',
            field=models.CharField(default=b'new', max_length=10, verbose_name=b'Information status', choices=[(b'new', b'New'), (b'verified', b'Verified'), (b'updated', b'Updated'), (b'certified', b'Certified'), (b'archived', b'Archived'), (b'deleted', b'Deleted')]),
        ),
    ]
