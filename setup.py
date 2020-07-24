#!/usr/bin/env python

import codecs
import os.path
import re
from setuptools import setup


base_dir = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(base_dir, 'i2c_lcd', '__init__.py')) as stream:
    data = stream.read()
    version = re.search(r'__version__\s*=\s*\'(.+)\'', data).group(1)
    author = re.search(r'__author__\s*=\s*\'(.+)\'', data).group(1)


setup(
    name='i2c_lcd',
    author=author,
    version=version,
    description='Package for control 1-line/2-line lcd display via i2c interface',
    long_description=open(os.path.join(base_dir, 'README.md')).read(),
    packages=['i2c_lcd'],
    entry_points={
        'console_scripts': [
            'lcd-init=i2c_lcd.entry:init_lcd',
            'lcd-display-ip=i2c_lcd.entry:display_ip',
            'lcd-backlight=i2c_lcd.entry:switch_backlight',
            'lcd-write=i2c_lcd.entry:write',
            'lcd-clear=i2c_lcd.entry:clear'
        ]
    },
    install_requires=open(os.path.join(base_dir, 'requirements.txt')).readlines()
)
