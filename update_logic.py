from models import *
from xmi_parser import TangoXmiParser


def documentation_update(update_object, activity, device_server, backup_device_server=None):
    # check documentation
    # readme is update directly
    if update_object.upload_readme:
        device_server.readme = update_object.readme_file

    # old documentation will be
    current_docs = device_server.documentation.filter(invalidate_activity=None)

    new_documentation = DeviceServerDocumentation(documentation_type=update_object.documentation1_type,
                                                  url=update_object.documentation1_url,
                                                  title=update_object.documentation1_title,
                                                  documentation_file=update_object.documentation1_file,
                                                  create_activity=activity,
                                                  device_server=device_server)

    if update_object.documentation1_pk is not None:
        doc = current_docs.filter(pk=update_object.documentation1_pk).first()
        if doc is not None and (not update_object.script_operation or doc.updated_by_script()):
            if update_object.other_documentation1:

                assert isinstance(doc, DeviceServerDocumentation)

                if doc.documentation_type != update_object.documentation1_type \
                        or update_object.documentation1_file is not None \
                        or update_object.documentation1_url != doc.url \
                        or update_object.documentation1_title != doc.title:

                    new_documentation.save()

                    if backup_device_server is not None:
                        doc.device_server = backup_device_server
                        doc.make_invalid(activity=activity)
                        doc.save()
                    else:
                        doc.make_invalid(activity=activity)
                        doc.save()

            else:
                if backup_device_server is not None:
                    doc.device_server = backup_device_server
                doc.make_invalid(activity=activity)
                doc.save()

    elif update_object.other_documentation1:
        new_documentation.save()

    # doc 2
    new_documentation = DeviceServerDocumentation(documentation_type=update_object.documentation2_type,
                                                  url=update_object.documentation2_url,
                                                  title=update_object.documentation2_title,
                                                  documentation_file=update_object.documentation2_file,
                                                  create_activity=activity,
                                                  device_server=device_server)

    if update_object.documentation2_pk is not None:
        doc = current_docs.filter(pk=update_object.documentation2_pk).first()
        if doc is not None and (not update_object.script_operation or doc.updated_by_script()):
            if update_object.other_documentation2:

                assert isinstance(doc, DeviceServerDocumentation)

                if doc.documentation_type != update_object.documentation2_type \
                        or update_object.documentation2_file is not None \
                        or update_object.documentation2_url != doc.url \
                        or update_object.documentation2_title != doc.title:

                    new_documentation.save()

                    if backup_device_server is not None:
                        doc.device_server = backup_device_server
                        doc.make_invalid(activity=activity)
                        doc.save()
                    else:
                        doc.make_invalid(activity=activity)
                        doc.save()

            else:
                if backup_device_server is not None:
                    doc.device_server = backup_device_server
                doc.make_invalid(activity=activity)
                doc.save()

    elif update_object.other_documentation2:
        new_documentation.save()

    # doc 3
    new_documentation = DeviceServerDocumentation(documentation_type=update_object.documentation3_type,
                                                  url=update_object.documentation3_url,
                                                  title=update_object.documentation3_title,
                                                  documentation_file=update_object.documentation3_file,
                                                  create_activity=activity,
                                                  device_server=device_server)

    if update_object.documentation3_pk is not None:
        doc = current_docs.filter(pk=update_object.documentation3_pk).first()
        if doc is not None and (not update_object.script_operation or doc.updated_by_script()):
            if update_object.other_documentation1:

                assert isinstance(doc, DeviceServerDocumentation)

                if doc.documentation_type != update_object.documentation3_type \
                        or update_object.documentation3_file is not None \
                        or update_object.documentation3_url != doc.url \
                        or update_object.documentation3_title != doc.title:

                    new_documentation.save()

                    if backup_device_server is not None:
                        doc.device_server = backup_device_server
                        doc.make_invalid(activity=activity)
                        doc.save()
                    else:
                        doc.make_invalid(activity=activity)
                        doc.save()

            else:
                if backup_device_server is not None:
                    doc.device_server = backup_device_server
                doc.make_invalid(activity=activity)
                doc.save()

    elif update_object.other_documentation3:
        new_documentation.save()


def repository_update(update_object, activity, device_server, backup_device_server=None):
    """ Updates/creates repository in the device server from update/add model"""

    # check repository
    new_repository = None
    if update_object.available_in_repository or update_object.repository_contact is not None \
            or update_object.repository_download_url is not None:
        if not update_object.available_in_repository:
            update_object.repository_type = None
            update_object.repository_url = None
            update_object.repository_path = None
            update_object.repository_download_url = None
            update_object.repository_tag = None
        new_repository = DeviceServerRepository(repository_type=update_object.repository_type,
                                                url=update_object.repository_url,
                                                path_in_repository=update_object.repository_path,
                                                contact_email=update_object.repository_contact,
                                                download_url=update_object.repository_download_url,
                                                tag=update_object.repository_tag
                                                )
        if backup_device_server is not None:
            # if it is update operation and repository change old repo is redirected to backup device server
            # and new_repository is marked as update
            if hasattr(device_server, 'repository'):
                assert isinstance(device_server.repository, DeviceServerRepository)
                # check also if there is a real change
                if new_repository.repository_type != device_server.repository.repository_type \
                        or new_repository.url != device_server.repository.url \
                        or new_repository.path_in_repository != device_server.repository.path_in_repository \
                        or new_repository.download_url != device_server.repository.download_url \
                        or new_repository.tag != device_server.repository.tag \
                        or new_repository.contact_email != device_server.repository.contact_email:
                    # for modified repository move it to backup
                    old_repo = device_server.repository
                    old_repo.device_server = backup_device_server
                    old_repo.invalidate_activity = activity
                    old_repo.save()
                    new_repository.last_update_activity = activity
                    new_repository.device_server = device_server
                    new_repository.create_activity = old_repo.create_activity

                else:
                    # no real change
                    new_repository = None
        else:
            # here, it means we are creating a new device server
            new_repository.create_activity = activity
            new_repository.device_server = device_server

    # make sure the repository is saved
    if new_repository is not None:
        new_repository.last_update_activity = activity
        new_repository.device_server = device_server

        new_repository.save()


def create_or_update(update_object, activity, device_server=None, device_class=None):
    """this method creates or updates device server based on update/add object. It should be used inside atimic
    transaction to keep database consistent.
        :return (device_server, backup_device_server)
    """

    assert isinstance(update_object, DeviceServerAddModel)

    backup_device_server = None
    new_device_server = None
    parser = None

    # backup device server if it is update
    if device_server is not None:
        backup_device_server = device_server.make_backup(activity=activity)
        backup_device_server.save()

    # basic information about device server
    if update_object.use_uploaded_xmi_file or update_object.use_url_xmi_file:
        # use xmi file
        xmi_string, ok, message = update_object.xmi_string()
        print '-------------'
        print message
        if ok:
            parser = TangoXmiParser(xml_string=xmi_string)
            # device server object
            new_device_server = parser.get_device_server()

    else:
        new_device_server = DeviceServer(name='', description='')

    if update_object.certified is not None:
        new_device_server.certified = update_object.certified

    if update_object.development_status is not None:
        new_device_server.development_status = update_object.development_status

    if update_object.ds_status is not None:
        new_device_server.status = update_object.ds_status

    if update_object.picture is not None:
        new_device_server.picture = update_object.picture

    if update_object.ds_info_copy:
        new_device_server.description = ''
        if not update_object.use_url_xmi_file and not update_object.use_uploaded_xmi_file \
                and len(update_object.class_name) > 0:
            new_device_server.name = update_object.class_name
            if len(update_object.license_name) > 0:
                lic = DeviceServerLicense.objects.get_or_create(name=update_object.license_name)[0]
                if lic.pk is None:
                    lic.save()
                new_device_server.license = lic

    # if data provided manually
    if not update_object.ds_info_copy:
        new_device_server.name = update_object.name
        new_device_server.description = update_object.description

    # make sure license object is saved
    if new_device_server.license is not None and new_device_server.license.pk is None:
        new_device_server.license.save()

    # so, we have base information
    if device_server is None:
        device_server = new_device_server
        device_server.create_activity = activity
        device_server.created_by = activity.created_by
        device_server.status = STATUS_NEW
    else:
        if not update_object.ds_info_copy or update_object.use_manual_info or update_object.use_url_xmi_file or \
                update_object.use_uploaded_xmi_file or \
                (update_object.ds_info_copy and new_device_server.name != device_server.name):
            # the if above is to avoid update when not asked for
            device_server.name = new_device_server.name
            device_server.description = new_device_server.description
            device_server.license = new_device_server.license
        device_server.last_update_activity = activity
        device_server.development_status = new_device_server.development_status
        device_server.certified = new_device_server.certified
        device_server.status = STATUS_UPDATED
        if new_device_server.picture is not None:
            device_server.picture = new_device_server.picture

    # make sure device server has pk
    device_server.save()

    # # mark it in activity
    # activity.device_server = device_server
    # activity.device_server_backup = backup_device_server
    # activity.save()

    repository_update(update_object, activity, device_server, backup_device_server)

    # call update documentation
    documentation_update(update_object, activity, device_server, backup_device_server)

    # get classes and interface
    if (update_object.use_uploaded_xmi_file or update_object.use_url_xmi_file) and parser is not None:
        # for xmi file all old device classes and relation are moved to backup and new are created from scratch
        if not update_object.add_class:
            if device_class is None:
                for cl in device_server.device_classes.all():
                    cl.make_invalid(activity)
                    if backup_device_server is not None:
                        cl.device_server = backup_device_server
                    cl.save()
            else:
                cl = device_server.device_classes.filter(pk=device_class).first()
                cl.make_invalid(activity)
                if backup_device_server is not None:
                    cl.device_server = backup_device_server
                cl.save()

        # read classes from xmi file
        cls = parser.get_device_classes()
        for cl in cls:
            # save class
            assert (isinstance(cl, DeviceClass))
            cl.device_server = device_server
            cl.create_activity = activity
            if backup_device_server is not None:
                cl.last_update_activity = activity
            if cl.license is not None and cl.license.pk is None:
                cl.license.save()

            cl.save()

            # create and save class info object
            class_info = parser.get_device_class_info(cl)
            assert (isinstance(class_info, DeviceClassInfo))
            class_info.device_class = cl
            class_info.save()  # need to do it to be able to populate m2m field
            class_info.additional_families.clear()
            class_info.additional_families.add(*update_object.additional_families.all())
            class_info.create_activity = activity
            if backup_device_server is not None:
                class_info.last_update_activity = activity

            # if manual info provided override defaults
            if update_object.use_manual_info:
                if len(update_object.contact_email) > 0:
                    class_info.contact_email = update_object.contact_email

            class_info.save()

            # create and save attributes
            attributes = parser.get_device_attributes(cl)
            for attrib in attributes:
                assert (isinstance(attrib, DeviceAttribute))
                attrib.device_class = cl
                attrib.create_activity = activity
                attrib.save()

            # create and save commands
            commands = parser.get_device_commands(cl)
            for command in commands:
                assert (isinstance(command, DeviceCommand))
                command.device_class = cl
                command.create_activity = activity
                command.save()

            # create and save pipes
            pipes = parser.get_device_pipes(cl)
            for pipe in pipes:
                assert (isinstance(pipe, DevicePipe))
                pipe.device_class = cl
                pipe.create_activity = activity
                pipe.save()

            # create and save properties
            properties = parser.get_device_properties(cl)
            for prop in properties:
                assert (isinstance(prop, DeviceProperty))
                prop.device_class = cl
                prop.create_activity = activity
                prop.save()

    elif update_object.use_manual_info:
        if backup_device_server is not None and not update_object.add_class:
            if device_class is None:
                clq = device_server.device_classes.all()
            else:
                clq = device_server.device_classes.filter(pk=device_class)

            for cl in clq:
                clo = cl.make_backup(activity)
                clo.device_server = backup_device_server
                clo.save()
                if hasattr(cl, 'info'):
                    cloi = cl.info.make_backup(activity, clo)
                    cloi.save()

        # manual info provided
        if device_class is None:
            clq = device_server.device_classes.all()

        else:
            clq = device_server.device_classes.filter(pk=device_class)

        if clq.count() > 0 and not update_object.add_class:
            cl = clq.first()
            cl.last_update_activity = activity
            cl_info = cl.info
            cl_info.last_update_activity = activity
        else:
            cl = DeviceClass()
            cl.create_activity = activity
            cl_info = DeviceClassInfo()
            cl_info.create_activity = activity
            if backup_device_server is not None:
                cl.last_update_activity = activity
                cl_info.last_update_activity = activity

        cl.name = update_object.class_name
        cl.description = update_object.class_description
        cl.class_copyright = update_object.class_copyright
        cl.language = update_object.language
        cl.device_server = device_server

        if len(update_object.license_name) > 0:
            lic = DeviceServerLicense.objects.get_or_create(name=update_object.license_name)[0]
            if lic.pk is None:
                lic.save()
            cl.license = lic

        cl.save()

        cl_info.device_class = cl
        cl_info.contact_email = update_object.contact_email
        cl_info.class_family = update_object.class_family
        cl_info.platform = update_object.platform
        cl_info.bus = update_object.bus
        cl_info.manufacturer = update_object.manufacturer
        cl_info.product_reference = update_object.product_reference
        cl_info.key_words = update_object.key_words
        cl_info.save()  # make sure to that cl_inf has a valid id
        cl_info.additional_families.clear()
        cl_info.additional_families.add(*update_object.additional_families.all())

        cl_info.save()

    # return device_server
    return device_server, backup_device_server
