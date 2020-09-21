# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


families_list = [
    'AbstractClasses', 'AcceleratorComponents', 'Acquisition', 'Application', 'Archiving', 'BeamDiagnostics',
    'BeamlineComponents', 'Calculation', 'Communication', 'Controllers', 'CounterTimer', 'InputOutput',
    'Instrumentation', 'Interlock', 'MagneticDevices', 'MeasureInstruments', 'Miscellaneous', 'Monitor',
    'Motion', 'OtherInstruments', 'PLC', 'PowerSupply', 'REST', 'RadioProtection', 'SampleEnvironment',
    'Security', 'Simulators', 'SoftwareSystem', 'StandardInterfaces', 'System', 'Temperature', 'Training',
    'Vacuum'
]


def fill_families(apps, schema_editor):
    # adds families to table

    # get django model for DevcieClassFamily
    family_model = apps.get_model("dsc", "DeviceClassFamily")

    # iterate throug the list of families
    for family_name in families_list:
        # get or create instance (to prevent creation of duplicates)
        f, created = family_model.objects.get_or_create(family=family_name)
        # if the instance is the new one save it
        if created:
            f.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0052_deviceserveraddmodel_additional_families'),
    ]

    operations = [
        migrations.RunPython(fill_families),
    ]
