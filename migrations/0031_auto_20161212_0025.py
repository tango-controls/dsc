# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0030_auto_20161211_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='use_url_xmi_file',
            field=models.BooleanField(default=False, verbose_name=b'Provide .xmi file URL populate database.'),
        ),
    ]
