# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0005_auto_20161030_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicecommand',
            name='input_description',
            field=models.TextField(null=True, verbose_name=b'Argin description', blank=True),
        ),
        migrations.AddField(
            model_name='devicecommand',
            name='output_description',
            field=models.TextField(null=True, verbose_name=b'Argout description', blank=True),
        ),
        migrations.AddField(
            model_name='deviceproperty',
            name='is_class_property',
            field=models.BooleanField(default=False, verbose_name=b'Class property'),
        ),
        migrations.AlterField(
            model_name='deviceclass',
            name='class_copyright',
            field=models.CharField(default=b'', max_length=128, verbose_name=b'Copyright', blank=True),
        ),
    ]
