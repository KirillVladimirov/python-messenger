#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'gbserver', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in aiohttpdemo_chat/__init__.py'
            raise RuntimeError(msg)


install_requires = [
    'aiohttp',
    'aiohttp_security',
    'cchardet',
    'aiodns',
]

setup(name='gbserver',
      version=read_version(),
      description='A simple server written for educational purposes to study python and asyncio.',
      platforms=['POSIX'],
      packages=['gbserver'],
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False)
