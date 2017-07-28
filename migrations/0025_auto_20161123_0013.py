# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import dsc.models as dsc_models


ADMINISTRATION_MODELS = ['DeviceServersActivityPluginModel']


def add_dsc_permissions(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    ContentType = apps.get_model("contenttypes", "ContentType")

    anonymous = User.objects.using(db_alias).get(username='anonymous')
    members = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_MEMBER)
    managers = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_CHIEF_EDITOR)
    administrators = Group.objects.using(db_alias).get(name=settings.TANGO_GROUP_ADMIN)


    administrators_perms = ()

    for model_code in ADMINISTRATION_MODELS:
        ct = ContentType.objects.get_for_model(getattr(dsc_models, model_code))

        administrators_perms += (
            Permission.objects.using(db_alias).get_or_create(codename='add_' + model_code.lower(),
                                                             content_type=ct,
                                                             defaults={'name': 'Can add ' + model_code})[0],

            Permission.objects.using(db_alias).get_or_create(codename='change_' + model_code.lower(),
                                                             defaults={'name': 'Can change ' + model_code},
                                                             content_type=ct)[0],

            Permission.objects.using(db_alias).get_or_create(codename='delete_' + model_code.lower(),
                                                             defaults={'name': 'Can delete ' + model_code},
                                                             content_type=ct)[0],
        )

    # print members_perms
    # print ''
    # print managers_perms

    administrators.permissions.add(*administrators_perms)


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0024_auto_20161123_0006'),
    ]

    operations = [
        migrations.RunPython(add_dsc_permissions),
    ]
