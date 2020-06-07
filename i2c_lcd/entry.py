"""Few samples and entry points for lcd.I2CLcd."""

from __future__ import unicode_literals

__author__ = 'Boris Polyanskiy'


import argparse
import socket
import time
import typing

from i2c_lcd.lcd import I2CLcd


def get_ip():
    # type: () -> typing.Text
    """Detect current IP address. If can't detect - return 127.0.0.1."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def display_ip():
    # type: () -> None
    """Detect IP address and show it on the LCD."""
    try:
        lcd = I2CLcd(hot_start=True)
    except OSError:
        print('I2C lcd not connected!')
        return

    while True:
        ip = get_ip()
        lcd.clear_display()
        if ip == '127.0.0.1':
            lcd.set_cursor()
            lcd.write('Loaded')
            lcd.set_cursor(2, 1)
            lcd.write('Wait ip: {:02d}'.format(10))
            for x in reversed(range(10)):
                lcd.set_cursor(2, 10)
                lcd.write('{:02d}'.format(x))
                time.sleep(1)
            continue

        lcd.set_cursor()
        lcd.write('Loaded')
        lcd.set_cursor(2, 1)
        lcd.write(ip)
        break


def init_lcd():
    # type: () -> None
    """Initialize the LCD."""
    I2CLcd(hot_start=False)


def switch_backlight():
    # type: () -> None
    """Switch a backlight of the LCD. Pass "on"/"off" as first argument to enable/disable a backlight."""
    parser = argparse.ArgumentParser()
    parser.add_argument('state', choices=['on', 'off'])
    args = parser.parse_args()
    lcd = I2CLcd(hot_start=True)
    lcd.set_backlight(args.state == 'on')


def write():
    # type: () -> None
    """Write string from first argument to the LCD. Use "--line num" to select line number."""
    parser = argparse.ArgumentParser()
    parser.add_argument('string')
    parser.add_argument('--line', type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    lcd = I2CLcd(hot_start=True)
    lcd.set_cursor(line=args.line)
    lcd.write(args.string)


def clear():
    # type: () -> None
    """Clear the display of the LCD."""
    lcd = I2CLcd()
    lcd.clear_display()
