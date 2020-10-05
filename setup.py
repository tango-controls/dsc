#!/usr/bin/env python2.7
import os
import subprocess

try:
    from setuptools import setup, find_packages
except ImportError:
    print("Cannot find setuptools; dependencies will not be installed.")
    from distutils.core import setup


setup(
    name="dsc",
    version=1.0,
    description="Device Server Catalogue for Tango Controls website",
    author="Tango Community",
    author_email="contact@tango-controls.org",
    url="http://www.tango-controls.org/developers/dsc/",
    packages=find_packages(),
   # package_dir={"dsc": "."},
    include_package_data=True,
    zip_safe=False
)
