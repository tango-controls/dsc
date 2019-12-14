#!/usr/bin/env python2.7

import subprocess
version = subprocess.check_output(["git", "describe", "--tags", "--always"])[:-1]

try:
	from setuptools import setup
except ImportError:
	print "Cannot find setuptools; dependencies will not be installed."
	from distutils.core import setup


setup(
	name="tango-website-plugin-dsc",
	version=version,
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
	# package_data={"dsc": [
	# 	"README.md",
	# 	"static/*/*",
	# 	"templates/*/*",
	# 	"tests/*.xmi"
	# ]},
	# data_files={"dsc": [
	# 	"README.md",
	# 	"static/*",
	# 	"templates/*",
	# 	"tests/*.xmi"
	# ]},
	include_package_data=True,
	zip_safe=False
)
