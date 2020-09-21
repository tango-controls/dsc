import dsc.tests.xmi_parser_test

def run():
    print "########################################################"
    print "Manual tests for xmi_parser.py"
    print "########################################################"
    print ""
    print "----------------------------"
    print "the first example of xmi file:"
    print ""
    dsc.tests.xmi_parser_test.manual_tests('src/dsc/tests/FirstLevelClass.xmi')
    print ""
    print "----------------------------"
    print "the second example of xmi file:"
    print ""
    dsc.tests.xmi_parser_test.manual_tests('src/dsc/tests/SecondLevelClass.xmi')
    print ""
    print "----------------------------"
    print "the third example of xmi"
    print ""
    dsc.tests.xmi_parser_test.manual_tests('src/dsc/tests/SecondLevleClass2.xmi')
    print ""
    print "----------------------------"
    print "Parsing original TangoTest.xmi"
    print ""
    dsc.tests.xmi_parser_test.manual_tests('src/dsc/tests/TangoTest.xmi')

    print ""
    print "end of manual tests of xmi_parser.py"
    print "#########################################################"