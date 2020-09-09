# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0038_auto_20161215_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='class_family',
            field=models.CharField(default=b'', max_length=128, null=True, blank=True),
        ),
    ]
