# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0036_deviceserveraddmodel_ds_info_copy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceattribute',
            name='data_type',
            field=models.SlugField(default=b'DevString', verbose_name=b'Data Type', choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevChar', b'DevChar'), (b'DevEncoded', b'DevEncoded'), (b'DevBoolean', b'DevBoolean'), (b'DevString', b'DevString'), (b'DevLong64', b'DevLong64'), (b'DevFloat', b'DevFloat'), (b'DevShort', b'DevShort'), (b'DevUChar', b'DevUChar'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')]),
        ),
    ]
