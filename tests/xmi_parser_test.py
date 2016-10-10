from django.test.utils import override_settings
from cms.test_utils.testcases import CMSTestCase

import dsc.models as dm
from dsc.xmi_parser import  TangoXmiParser


class XMIparserTest(CMSTestCase):

    general_test_file = 'FirstLevelClass.xmi'
    first_level_xmi_file = 'FirstLevelClass.xmi'

    def test_xmi_parser_creation(self):
        parser = TangoXmiParser(self.general_test_file)
        self.assertEqual(parser.tree.docinfo.xml_version,"1.0")
