#!/usr/bin/env python

from setuptools import setup

from i2c_lcd import __author__


setup(
    name='i2c_lcd',
    author=__author__,
    description='Package for control 1-line/2-line lcd display via i2c interface',
    long_description=open('README.md').read(),
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
    install_requires=open('requirements.txt').readlines()
)
