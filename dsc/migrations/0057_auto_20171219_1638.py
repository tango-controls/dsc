# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0056_deviceserveroldpluginmodel_deviceserversearchpluginmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DscGitHubBackupConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('oauth_id', models.CharField(max_length=128, verbose_name=b'OAuth id')),
                ('oauth_token', models.CharField(max_length=128, verbose_name=b'OAuth token')),
                ('repository_owner', models.CharField(default=b'tango-controls', max_length=255, verbose_name=b'Repository')),
                ('repository_name', models.CharField(default=b'dsc', max_length=255, verbose_name=b'Repository')),
                ('branch', models.CharField(default=b'xmi-backup', max_length=255, verbose_name=b'Branch')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='deviceserveractivity',
            name='activity_type',
            field=models.CharField(max_length=10, verbose_name=b'Activity', choices=[(b'add', b'Created'), (b'edit', b'Updated'), (b'download', b'Downloaded'), (b'delete', b'Deleted'), (b'apply_for_cert', b'Applied for certification'), (b'certify', b'Certificated'), (b'verify', b'Verified'), (b'verify', b'Reverted')]),
        ),
    ]
