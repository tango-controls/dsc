# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0047_auto_20170127_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation1_pk',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation2_pk',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='deviceserveraddmodel',
            name='documentation3_pk',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
