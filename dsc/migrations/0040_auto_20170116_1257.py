# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0039_auto_20161215_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceattribute',
            name='data_type',
            field=models.SlugField(default=b'DevString', verbose_name=b'Data Type', choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevChar', b'DevChar'), (b'DevEncoded', b'DevEncoded'), (b'DevBoolean', b'DevBoolean'), (b'DevString', b'DevString'), (b'DevLong64', b'DevLong64'), (b'DevState', b'DevState'), (b'DevFloat', b'DevFloat'), (b'DevShort', b'DevShort'), (b'DevUChar', b'DevUChar'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')]),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='input_type',
            field=models.SlugField(choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevVarDoubleStringArray', b'DevVarDoubleStringArray'), (b'DevChar', b'DevChar'), (b'DevBoolean', b'DevBoolean'), (b'DevVarUShortArray', b'DevVarUShortArray'), (b'DevString', b'DevString'), (b'DevFloat', b'DevFloat'), (b'DevVarStringArray', b'DevVarStringArray'), (b'DevVarLongStringArray', b'DevVarLongStringArray'), (b'DevVarLongArray', b'DevVarLongArray'), (b'DevVarShortArray', b'DevVarShortArray'), (b'DevVarLong64Array', b'DevVarLong64Array'), (b'DevVarULongArray', b'DevVarULongArray'), (b'DevUChar', b'DevUChar'), (b'State', b'State'), (b'DevVarULong64Array', b'DevVarULong64Array'), (b'ConstDevString', b'ConstDevString'), (b'DevVarCharArray', b'DevVarCharArray'), (b'DevVarFloatArray', b'DevVarFloatArray'), (b'DevLong64', b'DevLong64'), (b'DevVarDoubleArray', b'DevVarDoubleArray'), (b'DevVoid', b'DevVoid'), (b'DevShort', b'DevShort'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')], blank=True, null=True, verbose_name=b'Argument Type'),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='output_type',
            field=models.SlugField(choices=[(b'DevULong', b'DevULong'), (b'DevULong64', b'DevULong64'), (b'DevLong', b'DevLong'), (b'DevVarDoubleStringArray', b'DevVarDoubleStringArray'), (b'DevChar', b'DevChar'), (b'DevBoolean', b'DevBoolean'), (b'DevVarUShortArray', b'DevVarUShortArray'), (b'DevString', b'DevString'), (b'DevFloat', b'DevFloat'), (b'DevVarStringArray', b'DevVarStringArray'), (b'DevVarLongStringArray', b'DevVarLongStringArray'), (b'DevVarLongArray', b'DevVarLongArray'), (b'DevVarShortArray', b'DevVarShortArray'), (b'DevVarLong64Array', b'DevVarLong64Array'), (b'DevVarULongArray', b'DevVarULongArray'), (b'DevUChar', b'DevUChar'), (b'State', b'State'), (b'DevVarULong64Array', b'DevVarULong64Array'), (b'ConstDevString', b'ConstDevString'), (b'DevVarCharArray', b'DevVarCharArray'), (b'DevVarFloatArray', b'DevVarFloatArray'), (b'DevLong64', b'DevLong64'), (b'DevVarDoubleArray', b'DevVarDoubleArray'), (b'DevVoid', b'DevVoid'), (b'DevShort', b'DevShort'), (b'DevDouble', b'DevDouble'), (b'DevUShort', b'DevUShort')], blank=True, null=True, verbose_name=b'Output Type'),
        ),
    ]
