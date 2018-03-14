#!/usr/bin/env python

import pip
from distutils.core import setup
from setuptools import find_packages
import os

setup(
    name='Shipper',
    version='0.1dev',
    packages=find_packages(),
    license='',
    long_description=open(os.getcwd() + '/../README.md').read(),
)
