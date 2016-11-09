# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

BASE_MODELS = ['deviceserver', 'deviceclass', 'deviceclassinfo',
               'deviceserverdocumentation', 'deviceserverlicense', 'deviceserverrepository',
               'deviceattribute', 'devicecommand', 'devicepipe', 'deviceproperty']

ADMINISTRATION_MODELS = ['deviceserveractivity', 'deviceserveraddmodel', 'deviceserverpluginmodel']


def add_dsc_permissions_for_owners(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    anonymous = User.objects.using(db_alias).get(username='anonymous')
    members = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_MEMBER)
    managers = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_CHIEF_EDITOR)
    administrators = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_ADMIN)

    members_perms = (
        Permission.objects.using(db_alias).get(codename='update_own_deviceserver'),
        Permission.objects.using(db_alias).get(codename='delete_own_deviceserver'),
    )

    managers_perms = members_perms

    administrators_perms = managers_perms


    members.permissions.add(*members_perms)
    managers.permissions.add(*managers_perms)
    administrators.permissions.add(*administrators_perms)


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0017_auto_20161109_2249'),
    ]

    operations = [
        migrations.RunPython(add_dsc_permissions_for_owners)
    ]
