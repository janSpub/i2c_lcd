"""Package to control 1-line/2-line LCD via i2c interface.
Contains base methods for i2c devices (i2c.py) and methods for the i2c LCD (lcd.py)
"""

__author__ = 'Boris Polyanskiy'
__version__ = '1.3'

from .lcd import I2CLcd
from .entry import display_ip
