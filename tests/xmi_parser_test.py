from django.test.utils import override_settings
from cms.test_utils.testcases import CMSTestCase

import dsc.models as dm
from dsc.xmi_parser import TangoXmiParser


class XMIparserTest(CMSTestCase):

    general_test_file = 'src/dsc/tests/FirstLevelClass.xmi'
    first_level_xmi_file = 'src/dsc/tests/FirstLevelClass.xmi'
    second_level_xmi_file2 = 'src/dsc/tests/SecondLevleClass2.xmi'

    def test_xmi_parser_creation(self):
        parser = TangoXmiParser(self.general_test_file)
        self.assertEqual(parser.tree.docinfo.xml_version,"1.0")


def manual_tests(xmi_file):
    # create parser
    parser = TangoXmiParser(xmi_file)
    print "xml_version is %s" % parser.tree.docinfo.xml_version

    ds = parser.get_device_server()

    print "Device server: %s, %s" % (ds.name, ds.description)
    print "Licnese: %s " % ds.license.name

    print "Classes: "
    print parser.classes_elements

    cls = parser.get_device_classes()
    for cl in cls:
        print ""
        print "******************************************"
        print "Class name: %s" % cl.name
        print "Class description: %s" % cl.description
        print "Class license: %s, description: %s, URL: %s" % (cl.license.name,
                                                               cl.license.description,
                                                               cl.license.url)

        print "Class language: %s" % cl.language

        cli = parser.get_device_class_info(cl)
        assert (isinstance(cli,dm.DeviceClassInfo))
        print "Class info xmi_file: %s" % cli.xmi_file
        print "Class info contact: %s" % cli.contact_email
        print "Class info family: %s" % cli.class_family
        print "Class info platform: %s" % cli.platform
        print "Class info hardware (manufacturer, product, bus): (%s, %s, %s)" % (cli.manufacturer,
                                                                                  cli.product_reference,
                                                                                  cli.bus)
        print "Class info key words: %s" % cli.key_words
        print ""
        print "-------------Interface-----------------"
        print 'Class attributes (name, description):'
        attributes =parser.get_device_attributes(cl)
        for a in attributes:
            print "%s, %s" % (a.name, a.description)

        print 'Class commands (name, description):'
        attributes = parser.get_device_commands(cl)
        for a in attributes:
            print "%s, %s" % (a.name, a.description)

        print 'Class pipes (name, description):'
        attributes = parser.get_device_pipes(cl)
        for a in attributes:
            print "%s, %s" % (a.name, a.description)

        print 'Properties (name, description, is_class_property):'
        attributes = parser.get_device_properties(cl)
        for a in attributes:
            print "%s, %s, %s" % (a.name, a.description, a.is_class_property)

if __name__ == "__main__":
    manual_tests()
