# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0026_auto_20161207_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='repository_type',
            field=models.SlugField(choices=[(b'GIT', b'GIT'), (b'SVN', b'SVN'), (b'Mercurial', b'Mercurial'), (b'FTP', b'FTP'), (b'Other', b'Other')], blank=True, null=True, verbose_name=b'Repository Type'),
        ),
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='url',
            field=models.URLField(null=True, verbose_name=b'URL', blank=True),
        ),
    ]
