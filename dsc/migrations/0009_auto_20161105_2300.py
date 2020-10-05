# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0008_auto_20161105_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='repository_type',
            field=models.SlugField(default=b'', choices=[(b'GIT', b'GIT'), (b'SVN', b'SVN'), (b'Mercurial', b'Mercurial'), (b'FTP', b'FTP'), (b'Other', b'Other')], blank=True, verbose_name=b'Repository Type'),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='repository_url',
            field=models.URLField(default=b'', verbose_name=b'URL', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='use_manual_info',
            field=models.BooleanField(default=False, verbose_name=b'Provide data manually'),
        ),
    ]
