# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0004_auto_20161030_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceattribute',
            name='data_type',
            field=models.SlugField(default=b'DevString', verbose_name=b'Data Type', choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevChar', b'DevChar'), (b'DevBoolean', b'DevBoolean'), (b'DevString', b'DevString'), (b'DevLong64', b'DevLong64'), (b'DevFloat', b'DevFloat'), (b'DevShort', b'DevShort'), (b'DevUChar', b'DevUChar'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')]),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='input_type',
            field=models.SlugField(verbose_name=b'Argument Type', choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevVarDoubleStringArray', b'DevVarDoubleStringArray'), (b'DevChar', b'DevChar'), (b'DevBoolean', b'DevBoolean'), (b'DevVarUShortArray', b'DevVarUShortArray'), (b'DevString', b'DevString'), (b'DevFloat', b'DevFloat'), (b'DevVarStringArray', b'DevVarStringArray'), (b'DevVarLongStringArray', b'DevVarLongStringArray'), (b'DevVarLongArray', b'DevVarLongArray'), (b'DevVarShortArray', b'DevVarShortArray'), (b'DevVarLong64Array', b'DevVarLong64Array'), (b'DevVarULongArray', b'DevVarULongArray'), (b'DevUChar', b'DevUChar'), (b'DevVarULong64Array', b'DevVarULong64Array'), (b'DevVarCharArray', b'DevVarCharArray'), (b'DevVarFloatArray', b'DevVarFloatArray'), (b'DevLong64', b'DevLong64'), (b'DevVarDoubleArray', b'DevVarDoubleArray'), (b'DevShort', b'DevShort'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')]),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='output_type',
            field=models.SlugField(verbose_name=b'Output Type', choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevVarDoubleStringArray', b'DevVarDoubleStringArray'), (b'DevChar', b'DevChar'), (b'DevBoolean', b'DevBoolean'), (b'DevVarUShortArray', b'DevVarUShortArray'), (b'DevString', b'DevString'), (b'DevFloat', b'DevFloat'), (b'DevVarStringArray', b'DevVarStringArray'), (b'DevVarLongStringArray', b'DevVarLongStringArray'), (b'DevVarLongArray', b'DevVarLongArray'), (b'DevVarShortArray', b'DevVarShortArray'), (b'DevVarLong64Array', b'DevVarLong64Array'), (b'DevVarULongArray', b'DevVarULongArray'), (b'DevUChar', b'DevUChar'), (b'DevVarULong64Array', b'DevVarULong64Array'), (b'DevVarCharArray', b'DevVarCharArray'), (b'DevVarFloatArray', b'DevVarFloatArray'), (b'DevLong64', b'DevLong64'), (b'DevVarDoubleArray', b'DevVarDoubleArray'), (b'DevShort', b'DevShort'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')]),
        ),
        migrations.AlterField(
            model_name='deviceproperty',
            name='property_type',
            field=models.SlugField(verbose_name=b'Type', choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevChar', b'DevChar'), (b'DevBoolean', b'DevBoolean'), (b'DevString', b'DevString'), (b'DevLong64', b'DevLong64'), (b'DevFloat', b'DevFloat'), (b'DevShort', b'DevShort'), (b'DevUChar', b'DevUChar'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')]),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='path_in_repository',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Path', blank=True),
        ),
    ]
