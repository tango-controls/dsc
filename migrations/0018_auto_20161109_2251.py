# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings
import dsc.models as dsc_models



def add_dsc_permissions_for_owners(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    ContentType = apps.get_model("contenttypes", "ContentType")

    anonymous = User.objects.using(db_alias).get(username='anonymous')
    members = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_MEMBER)
    managers = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_CHIEF_EDITOR)
    administrators = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_ADMIN)

    ct = ContentType.objects.get_for_model(getattr(dsc_models, 'DeviceServer'))
    # if ct.pk is None:
    #     ct.save()

    members_perms = (
        Permission.objects.using(db_alias).get_or_create(codename='update_own_deviceserver',
                                               name='do changes to device server for creator',
                                               content_type=ct)[0],

        Permission.objects.using(db_alias).get_or_create(codename='delete_own_deviceserver',
                                               name='deletion of device server for creator',
                                               content_type=ct)[0],
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
