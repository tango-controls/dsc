# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings

import dsc.models as dsc_models

BASE_MODELS = []

ADMINISTRATION_MODELS = ['DeviceServerUpdateModel', 'DeviceClassFamily']


def add_dsc_permissions(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    # user_model = apps.get_model("auth", "User")
    group_model = apps.get_model("auth", "Group")
    permission_model = apps.get_model("auth", "Permission")

    content_type_model = apps.get_model("contenttypes", "ContentType")

    # anonymous = user_model.objects.using(db_alias).get(username='anonymous')
    members = group_model.objects.using(db_alias).get(name=settings.TANGO_GROUP_MEMBER)
    managers = group_model.objects.using(db_alias).get(name=settings.TANGO_GROUP_CHIEF_EDITOR)
    administrators = group_model.objects.using(db_alias).get(name=settings.TANGO_GROUP_ADMIN)

    ct = content_type_model.objects.get_for_model(getattr(dsc_models, 'DeviceServer'))
    # if ct.pk is None:
    #     ct.save()

    members_perms = (
        permission_model.objects.using(db_alias).get_or_create(codename='add_deviceserver',
                                                               defaults={'name': 'Can add DeviceServer'},
                                                               content_type=ct)[0],
    )

    managers_perms = members_perms + (
        permission_model.objects.using(db_alias).get_or_create(codename='admin_deviceserver',
                                                               defaults={'name':
                                                                 'do various administration tasks on device servers'},
                                                               content_type=ct)[0],
    )

    for model_code in BASE_MODELS:
        ct = content_type_model.objects.get_for_model(getattr(dsc_models, model_code))
        # if ct.pk is None:
        #     ct.save()

        managers_perms += (
            permission_model.objects.using(db_alias).get_or_create(codename='add_'+model_code.lower(),
                                                                   defaults={'name': 'Can add ' + model_code},
                                                                   content_type=ct)[0],

            permission_model.objects.using(db_alias).get_or_create(codename='change_'+model_code.lower(),
                                                                   defaults={'name': 'Can change ' + model_code},
                                                                   content_type=ct)[0],

            permission_model.objects.using(db_alias).get_or_create(codename='delete_'+model_code.lower(),
                                                                   defaults={'name': 'Can delete ' + model_code},
                                                                   content_type=ct)[0],
        )

    administrators_perms = managers_perms

    for model_code in ADMINISTRATION_MODELS:
        ct = content_type_model.objects.get_for_model(getattr(dsc_models, model_code))
        # print ct
        # if ct.pk is None:
        #     ct.save()

        administrators_perms += (
            permission_model.objects.using(db_alias).get_or_create(codename='add_' + model_code.lower(),
                                                                   defaults={'name': 'Can add ' + model_code},
                                                                   content_type=ct)[0],

            permission_model.objects.using(db_alias).get_or_create(codename='change_' + model_code.lower(),
                                                                   defaults={'name': 'Can change ' + model_code},
                                                                   content_type=ct)[0],

            permission_model.objects.using(db_alias).get_or_create(codename='delete_' + model_code.lower(),
                                                                   defaults={'name': 'Can delete ' + model_code},
                                                                   content_type=ct)[0],
        )

    members.permissions.add(*members_perms)
    managers.permissions.add(*managers_perms)
    administrators.permissions.add(*administrators_perms)


class Migration(migrations.Migration):

    dependencies = [
        ('dsc', '0053_families_names_add'),
    ]

    operations = [
        migrations.RunPython(add_dsc_permissions)
    ]
