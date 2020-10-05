# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0058_github_backup_config_admin_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dscgithubbackupconfig',
            name='repository_owner',
            field=models.CharField(default=b'tango-controls', max_length=255, verbose_name=b'Repository owner'),
        ),
    ]
