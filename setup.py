#!/usr/bin/env python2.7
import os
import subprocess
VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"])[:-1]

try:
    from setuptools import setup
except ImportError:
    print "Cannot find setuptools; dependencies will not be installed."
    from distutils.core import setup


def gen_data_files(*dirs):
    results = []

    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            for file_name in files:
                results.append(root + "/" + file_name)
    return {'': results}


setup(
    name="tango-website-plugin-dsc",
    version=VERSION,
    description="Device Server Catalogue for Tango Controls website",
    author="Tango Community",
    author_email="contact@tango-controls.org",
    url="http://www.tango-controls.org/developers/dsc/",
    packages=[
        "dsc",
        "dsc.migrations",
        "dsc.scripts",
        "dsc.templatetags",
        "dsc.tests"
    ],
    package_dir={"dsc": "."},
    package_data=gen_data_files('templates', 'static'),
    include_package_data=True,
    zip_safe=False
)
