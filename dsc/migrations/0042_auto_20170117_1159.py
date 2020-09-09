# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0041_deviceserveraddmodel_repository_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='ds_status',
            field=models.CharField(default=b'new', max_length=20, verbose_name=b'Information status', choices=[(b'new', b'New'), (b'verified', b'Verified'), (b'updated', b'Updated'), (b'certified', b'Certified'), (b'archived', b'Archived'), (b'deleted', b'Deleted')]),
        ),
    ]
