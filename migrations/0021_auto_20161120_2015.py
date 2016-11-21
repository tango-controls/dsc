# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0020_auto_20161120_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceproperty',
            name='property_type',
            field=models.SlugField(verbose_name=b'Type'),
        ),
    ]
