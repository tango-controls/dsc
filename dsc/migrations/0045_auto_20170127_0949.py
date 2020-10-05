# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0044_auto_20170126_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceserverpluginmodel',
            options={'verbose_name': 'Device Classes Catalogue plugin'},
        ),
        migrations.AlterModelOptions(
            name='deviceserversactivitypluginmodel',
            options={'verbose_name': 'Device Classes Catalogue Activity plugin'},
        ),
        migrations.AddField(
            model_name='deviceserverdocumentation',
            name='documentation_file',
            field=models.FileField(max_length=2000000, upload_to=b'dsc_readmes', null=True, verbose_name=b'Document', blank=True),
        ),
        migrations.AddField(
            model_name='deviceserverdocumentation',
            name='title',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Title', blank=True),
        ),
        migrations.AlterField(
            model_name='deviceserverdocumentation',
            name='url',
            field=models.URLField(default=b'', null=True, verbose_name=b'URL', blank=True),
        ),
    ]
