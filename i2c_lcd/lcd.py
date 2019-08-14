"""
Module to control 1-line/2-line lcd via i2c interface.
"""

from __future__ import unicode_literals

__author__ = 'Boris Polyanskiy'

from time import sleep
import typing

from i2c_lcd.i2c import I2CDevice


class I2CLcd(I2CDevice):
    """Class to control 1-line/2-line lcd via i2c interface."""

    def __init__(self, line2=True, dots5x11=False, hot_start=False):
        # type: (bool, bool, bool) -> None
        """

        :param line2: True for 2-line display, False for 1-line.
        :param dots5x11: True for 5x11 dots format display mode, False for 5x8.
        :param hot_start: True for skip lcd initialization, False - not.
        """

        I2CDevice.__init__(self, 0x27)
        self.__backlight = True
        self.__line = None

        # Initialize display
        if not hot_start:
            self._write(0b110011)
            self._write(0b110010)
            sleep(0.002)

        self.function_set(two_line=line2, dots_5x11=dots5x11)
        self.set_display()
        self.set_shift_mode()
        self.set_cursor()
        self.set_backlight()
        # self.clear_display()

    @property
    def backlight_bits(self):
        # type: () -> int
        """Backlight in command format (0b100 or 0b000)"""
        return self.__backlight << 3

    def clear_display(self):
        # type: () -> None
        """Clear display.
        Return cursor to original position if shifted (left edge on first line of the display).
        :return: None
        """

        self._write(0b1)

    def return_home(self):
        # type: () -> None
        """Return cursor to original position if shifted (left edge on first line of the display).
        :return: None
        """

        self._write(0b10)

    def set_shift_mode(self, display=False, reverse=False):
        # type: (bool, bool) -> None
        """Set cursor move mode or display shift. Also set direction of move/shift.

        In cursor move mode cursor will move to next position after writing character (display=False).
        In display shift mode cursor will stay on current position, but display will move to specified direction (
            display=True).
        In reverse move cursor/display will move right to left.

        | 1 | I/D | S |
        110 - cursor/blink moves to right.
        100 - cursor/blink moves to left.
        111 - shift of entire display to left.
        101 - shift of entire display to right.

        :param display: True for display shift mode, False for cursor move mode.
        :param reverse: True for move/shift direction left to right, False for right to left.
        :return: None
        """

        self._write(0b100 | display | (not reverse) << 1)

    def set_display(self, display=True, cursor=False, blink=False):
        # type: (bool, bool, bool) -> None
        """Set display parameters.

        | 1 | D | C | B |
        D - display (1 turned on, 0 turned off). It is not backlight!
        C - cursor (1 turned on, 0 turned off).
        B - cursor blink (1 blink is on, 0 blink is off).

        :param display: True for turn on display, False for turn off.
        :param cursor: True for turn on cursor, False for turn off.
        :param blink: True for enable blink, False for disable.
        :return: None
        """

        self._write(0b1000 | display << 2 | cursor << 1 | blink)

    def function_set(self, two_line=True, dots_5x11=False):
        # type: (bool, bool) -> None
        """Set lcd parameters.

        | 1 | DL | N | F | x | x |
        DL - interface data length control bit (1 - 8-bit bus, 0 - 4-bit bus).
         When 4-bit bus mode, it needs to transfer 4-bit data two times.
        N - display  line number control bit (1 - 2-line display mode, 1 - 1-line display mode).
        F - display font type control bit (1 - 5x11 dots format display mode, 0 - 5x8).

        :param two_line: True for 2-line display, False for 1-line.
        :param dots_5x11: True for 5x11 dots format display mode, False for 5x8.
        :return: None
        """

        self._write(0b100000 | two_line << 3 | dots_5x11 << 2)
        self.__line = two_line

    def set_cursor(self, line=1, position=1):
        # type: (int, int) -> None
        """Change cursor position.

        :param line: number of line of lcd (1 or 2).
        :param position: position in line.
        :return: None
        """

        position -= 1
        if line < 1 or line > (2 if self.__line else 1):
            raise ValueError('Line can be 1{}!'.format(' or 2' if self.__line else ''))
        if line == 2:
            position += 0x40
        # 0b10000000 - set DDRAM
        self._write(0b10000000 + position)

    def write_value(self, value):
        # type: (int) -> None
        """Display letter value (ord).

        :param value: letter's ord
        :return: None
        """
        self._write(value, data_mode=True)

    def write(self, string):
        # type: (typing.Text) -> None
        """Display string or letter on lcd (at current cursor position).

        Use ord(<int>) to use custom symbols (loaded in load_custom_char).

        :param string: string or letter.
        :return: None
        """

        for letter in string:
            self.write_value(ord(letter))

    def load_custom_char(self, data, position=0):
        # type: (typing.List[int], int) -> None
        """Load custom character to CGRAM.

        After load custom character you need to set position of cursor.

        Sample of data (arrow pointed to bottom):
        [
            0b01110,
            0b01110,
            0b01110,
            0b01110,
            0b11111,
            0b01110,
            0b00100
        ]

        :param data: list with integers, where each integer is a line in character.
        :param position: position in CGRAM (0-7)
        :return: None
        """

        # 0b1000000 - set CGRAM
        if position > 7 or position < 0:
            raise ValueError('Position can be 0-7!')
        self._write(0b1000000 + position * 8)
        for line in data:
            self._write(line, data_mode=True)

    def _write(self, value, data_mode=False):
        # type: (int, bool) -> None
        """Write byte (value) to lcd. Using 4-bit mode (split value to 2 4-bit packs).

        :param value: 8-bit data.
        :param data_mode: True for data mode, False for command mode.
        :return: None
        """

        mode = int(data_mode)
        bits_high = mode | (value & 0xF0) | self.backlight_bits
        bits_low = mode | ((value << 4) & 0xF0) | self.backlight_bits

        # High bits
        self.write_byte(bits_high)
        self.enable(bits_high)

        # Low bits
        self.write_byte(bits_low)
        self.enable(bits_low)

    def enable(self, value):
        # type: (int) -> None
        """Toggle enable."""
        enable_bit = 0b100

        sleep(0.0005)
        self.write_byte(value | enable_bit)
        sleep(0.0005)
        self.write_byte(value & ~enable_bit)
        sleep(0.0005)

    def set_backlight(self, enable=True):
        # type: (bool) -> None
        """Change lcd back light.

        :param enable: True to enable backlight, False to disable.
        :return: None
        """

        self.__backlight = bool(enable)
        self.write_byte(self.backlight_bits)

    def shift_cursor(self, left=False):
        # type: (bool) -> None
        """Shift cursor to selected direction.

        100xx - shift cursor to the left.
        101xx - shift cursor to the right.

        :param left: True for left direction, False for right
        :return: None
        """

        self._write(0b10000 | (not left) << 2)

    def shift_display(self, left=False):
        # type: (bool) -> None
        """Shift display to selected direction. Cursor follows the display shift.

        110xx - shift display to the left.
        111xx - shift display to the right.

        :param left: True for left direction, False for right
        :return: None
        """

        self._write(0b11000 | (not left) << 2)
