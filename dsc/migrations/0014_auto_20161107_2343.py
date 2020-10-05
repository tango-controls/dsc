# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0013_auto_20161107_0011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceserver',
            options={'permissions': (('add_deviceserver', 'add a new device server'), ('change_deviceserver', 'update existed device servers'), ('delete_deviceserver', 'delete device servers'), ('admin_deviceserver', 'do various administration tasks on device servers'))},
        ),
        migrations.AlterField(
            model_name='deviceserveractivity',
            name='activity_type',
            field=models.CharField(max_length=10, verbose_name=b'Activity', choices=[(b'add', b'Add'), (b'edit', b'Edit'), (b'download', b'Download'), (b'delete', b'Delete'), (b'apply_for_cert', b'Apply for cerification'), (b'certify', b'Certify'), (b'verification', b'Verification')]),
        ),
    ]
