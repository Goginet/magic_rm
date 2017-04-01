#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

from os.path import dirname, join

from setuptools import find_packages, setup

import magic_rm

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name='magic_rm',
    version=magic_rm.__version__,
    install_requires=install_requirements,
    packages=find_packages(), entry_points={
        'console_scripts':
            ['magic_rm = magic_rm.cmd:main']
    },
    long_description=open(join(dirname(__file__), 'README.md')).read(),
)
