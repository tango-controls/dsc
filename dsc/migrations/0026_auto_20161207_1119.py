# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0025_auto_20161123_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceserverrepository',
            name='repository_type',
            field=models.SlugField(null=True, verbose_name=b'Repository Type', choices=[(b'GIT', b'GIT'), (b'SVN', b'SVN'), (b'Mercurial', b'Mercurial'), (b'FTP', b'FTP'), (b'Other', b'Other')]),
        ),
    ]
