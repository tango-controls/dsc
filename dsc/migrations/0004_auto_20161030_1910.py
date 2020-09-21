# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0003_auto_20160922_1112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceserver',
            options={},
        ),
        migrations.AddField(
            model_name='deviceclass',
            name='class_copyright',
            field=models.CharField(default=b'', max_length=128, verbose_name=b'Copyright'),
        ),
        migrations.AddField(
            model_name='deviceclass',
            name='language',
            field=models.CharField(default=b'Cpp', max_length=32, verbose_name=b'Language', choices=[(b'Cpp', b'Cpp'), (b'Python', b'Python'), (b'PythonHL', b'PythonHL'), (b'Java', b'Java'), (b'CSharp', b'CSharp'), (b'LabView', b'LabView')]),
        ),
        migrations.AddField(
            model_name='deviceclass',
            name='license',
            field=models.ForeignKey(related_name='licensed_device_classes', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'License', blank=True, to='dsc.DeviceServerLicense', null=True),
        ),
        migrations.AddField(
            model_name='deviceclassinfo',
            name='product_reference',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'Product'),
        ),
        migrations.AlterField(
            model_name='deviceattribute',
            name='attribute_type',
            field=models.SlugField(default=b'Scalar', verbose_name=b'Type', choices=[(b'Scalar', b'Scalar'), (b'Spectrum', b'Spectrum'), (b'Image', b'Image')]),
        ),
        migrations.AlterField(
            model_name='deviceattribute',
            name='data_type',
            field=models.SlugField(verbose_name=b'Data Type', choices=[((b'UIntType', b'DevULong'), (b'UIntType', b'DevULong')), ((b'ULongType', b'DevULong64'), (b'ULongType', b'DevULong64')), ((b'IntType', b'DevLong'), (b'IntType', b'DevLong')), ((b'CharType', b'DevChar'), (b'CharType', b'DevChar')), ((b'BooleanType', b'DevBoolean'), (b'BooleanType', b'DevBoolean')), ((b'StringType', b'DevString'), (b'StringType', b'DevString')), ((b'LongType', b'DevLong64'), (b'LongType', b'DevLong64')), ((b'FloatType', b'DevFloat'), (b'FloatType', b'DevFloat')), ((b'ShortType', b'DevShort'), (b'ShortType', b'DevShort')), ((b'UCharType', b'DevUChar'), (b'UCharType', b'DevUChar')), ((b'DoubleType', b'DevDouble'), (b'DoubleType', b'DevDouble')), ((b'UShortType', b'DevUShort'), (b'UShortType', b'DevUShort'))]),
        ),
        migrations.AlterField(
            model_name='deviceattribute',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceattribute',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='deviceclass',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceclass',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='bus',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Bus', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='class_family',
            field=models.CharField(default=b'', max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='contact_email',
            field=models.EmailField(max_length=254, verbose_name=b'Contact'),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='key_words',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Key words', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='manufacturer',
            field=models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Manufacturer'),
        ),
        migrations.AlterField(
            model_name='deviceclassinfo',
            name='platform',
            field=models.CharField(default=b'All Platforms', max_length=64, verbose_name=b'Platform', choices=[(b'Windows', b'Windows'), (b'Unix Like', b'Unix Like'), (b'All Platforms', b'All Platforms')]),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='input_type',
            field=models.SlugField(verbose_name=b'Argument Type', choices=[((b'UIntType', b'DevULong'), (b'UIntType', b'DevULong')), ((b'ULongType', b'DevULong64'), (b'ULongType', b'DevULong64')), ((b'IntType', b'DevLong'), (b'IntType', b'DevLong')), ((b'DoubleStringArrayType', b'DevVarDoubleStringArray'), (b'DoubleStringArrayType', b'DevVarDoubleStringArray')), ((b'CharType', b'DevChar'), (b'CharType', b'DevChar')), ((b'BooleanType', b'DevBoolean'), (b'BooleanType', b'DevBoolean')), ((b'UShortArrayType', b'DevVarUShortArray'), (b'UShortArrayType', b'DevVarUShortArray')), ((b'StringType', b'DevString'), (b'StringType', b'DevString')), ((b'FloatType', b'DevFloat'), (b'FloatType', b'DevFloat')), ((b'StringArrayType', b'DevVarStringArray'), (b'StringArrayType', b'DevVarStringArray')), ((b'LongStringArrayType', b'DevVarLongStringArray'), (b'LongStringArrayType', b'DevVarLongStringArray')), ((b'IntArrayType', b'DevVarLongArray'), (b'IntArrayType', b'DevVarLongArray')), ((b'ShortArrayType', b'DevVarShortArray'), (b'ShortArrayType', b'DevVarShortArray')), ((b'LongArrayType', b'DevVarLong64Array'), (b'LongArrayType', b'DevVarLong64Array')), ((b'UIntArrayType', b'DevVarULongArray'), (b'UIntArrayType', b'DevVarULongArray')), ((b'UCharType', b'DevUChar'), (b'UCharType', b'DevUChar')), ((b'ULongArrayType', b'DevVarULong64Array'), (b'ULongArrayType', b'DevVarULong64Array')), ((b'CharArrayType', b'DevVarCharArray'), (b'CharArrayType', b'DevVarCharArray')), ((b'FloatArrayType', b'DevVarFloatArray'), (b'FloatArrayType', b'DevVarFloatArray')), ((b'LongType', b'DevLong64'), (b'LongType', b'DevLong64')), ((b'DoubleArrayType', b'DevVarDoubleArray'), (b'DoubleArrayType', b'DevVarDoubleArray')), ((b'ShortType', b'DevShort'), (b'ShortType', b'DevShort')), ((b'DoubleType', b'DevDouble'), (b'DoubleType', b'DevDouble')), ((b'UShortType', b'DevUShort'), (b'UShortType', b'DevUShort'))]),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='output_type',
            field=models.SlugField(verbose_name=b'Output Type', choices=[((b'UIntType', b'DevULong'), (b'UIntType', b'DevULong')), ((b'ULongType', b'DevULong64'), (b'ULongType', b'DevULong64')), ((b'IntType', b'DevLong'), (b'IntType', b'DevLong')), ((b'DoubleStringArrayType', b'DevVarDoubleStringArray'), (b'DoubleStringArrayType', b'DevVarDoubleStringArray')), ((b'CharType', b'DevChar'), (b'CharType', b'DevChar')), ((b'BooleanType', b'DevBoolean'), (b'BooleanType', b'DevBoolean')), ((b'UShortArrayType', b'DevVarUShortArray'), (b'UShortArrayType', b'DevVarUShortArray')), ((b'StringType', b'DevString'), (b'StringType', b'DevString')), ((b'FloatType', b'DevFloat'), (b'FloatType', b'DevFloat')), ((b'StringArrayType', b'DevVarStringArray'), (b'StringArrayType', b'DevVarStringArray')), ((b'LongStringArrayType', b'DevVarLongStringArray'), (b'LongStringArrayType', b'DevVarLongStringArray')), ((b'IntArrayType', b'DevVarLongArray'), (b'IntArrayType', b'DevVarLongArray')), ((b'ShortArrayType', b'DevVarShortArray'), (b'ShortArrayType', b'DevVarShortArray')), ((b'LongArrayType', b'DevVarLong64Array'), (b'LongArrayType', b'DevVarLong64Array')), ((b'UIntArrayType', b'DevVarULongArray'), (b'UIntArrayType', b'DevVarULongArray')), ((b'UCharType', b'DevUChar'), (b'UCharType', b'DevUChar')), ((b'ULongArrayType', b'DevVarULong64Array'), (b'ULongArrayType', b'DevVarULong64Array')), ((b'CharArrayType', b'DevVarCharArray'), (b'CharArrayType', b'DevVarCharArray')), ((b'FloatArrayType', b'DevVarFloatArray'), (b'FloatArrayType', b'DevVarFloatArray')), ((b'LongType', b'DevLong64'), (b'LongType', b'DevLong64')), ((b'DoubleArrayType', b'DevVarDoubleArray'), (b'DoubleArrayType', b'DevVarDoubleArray')), ((b'ShortType', b'DevShort'), (b'ShortType', b'DevShort')), ((b'DoubleType', b'DevDouble'), (b'DoubleType', b'DevDouble')), ((b'UShortType', b'DevUShort'), (b'UShortType', b'DevUShort'))]),
        ),
        migrations.AlterField(
            model_name='devicepipe',
            name='description',
            field=models.TextField(verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='devicepipe',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='deviceproperty',
            name='description',
            field=models.TextField(verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceproperty',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='deviceproperty',
            name='property_type',
            field=models.SlugField(verbose_name=b'Type', choices=[((b'UIntType', b'DevULong'), (b'UIntType', b'DevULong')), ((b'ULongType', b'DevULong64'), (b'ULongType', b'DevULong64')), ((b'IntType', b'DevLong'), (b'IntType', b'DevLong')), ((b'CharType', b'DevChar'), (b'CharType', b'DevChar')), ((b'BooleanType', b'DevBoolean'), (b'BooleanType', b'DevBoolean')), ((b'StringType', b'DevString'), (b'StringType', b'DevString')), ((b'LongType', b'DevLong64'), (b'LongType', b'DevLong64')), ((b'FloatType', b'DevFloat'), (b'FloatType', b'DevFloat')), ((b'ShortType', b'DevShort'), (b'ShortType', b'DevShort')), ((b'UCharType', b'DevUChar'), (b'UCharType', b'DevUChar')), ((b'DoubleType', b'DevDouble'), (b'DoubleType', b'DevDouble')), ((b'UShortType', b'DevUShort'), (b'UShortType', b'DevUShort'))]),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='description',
            field=models.TextField(verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='deviceserver',
            name='status',
            field=models.CharField(default=b'new', max_length=10, verbose_name=b'Status'),
        ),
        migrations.AlterField(
            model_name='deviceserverdocumentation',
            name='documentation_type',
            field=models.SlugField(verbose_name=b'Documentation type', choices=[(b'README', b'README'), (b'Manual', b'Manual'), (b'InstGuide', b'Installation Guide'), (b'Generated', b'Generated'), (b'SourceDoc', b'Source Documentation')]),
        ),
        migrations.AlterField(
            model_name='deviceserverdocumentation',
            name='url',
            field=models.URLField(verbose_name=b'URL'),
        ),
        migrations.AlterField(
            model_name='deviceserverlicense',
            name='description',
            field=models.TextField(default=b'', null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserverlicense',
            name='name',
            field=models.CharField(max_length=64, serialize=False, verbose_name=b'License', primary_key=True),
        ),
        migrations.AlterField(
            model_name='deviceserverlicense',
            name='url',
            field=models.URLField(null=True, verbose_name=b'URL', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='path_in_repository',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Path', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='repository_type',
            field=models.SlugField(verbose_name=b'Repository Type', choices=[(b'GIT', b'GIT'), (b'SVN', b'SVN'), (b'Mercurial', b'Mercurial'), (b'FTP', b'FTP'), (b'Other', b'Other')]),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='url',
            field=models.URLField(verbose_name=b'URL'),
        ),
    ]
