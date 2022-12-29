#!/usr/bin/python3
# This file is an indicator that the module/package we are about to install
# has been packaged and distributed using some tool such as Distutils or 
# setuptools
from setuptools import setup, find_packages

setup(
	name = "LitCode",
	version = "0.0.1",
	packages = find_packages("litcode"),
	py_modules = ("litcode"),
	package_dir = {"": "litcode"},
	package_data = {"static": ["*.base"]},
	entry_points = {
		"console_scripts": ["litcode=litcode.app:main"]
	}
)