# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0022_auto_20161120_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceServerUpdateModel',
            fields=[
                ('deviceserveraddmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dsc.DeviceServerAddModel')),
            ],
            bases=('dsc.deviceserveraddmodel',),
        ),
        migrations.AlterField(
            model_name='deviceserveraddmodel',
            name='available_in_repository',
            field=models.BooleanField(default=True, verbose_name=b'Available in repository'),
        ),
    ]
