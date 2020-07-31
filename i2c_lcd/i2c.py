"""Methods for working with i2c devices."""

__author__ = 'Boris Polyanskiy'

from time import sleep
try:
    import smbus
except ImportError:
    import smbus2 as smbus


class I2CDevice:
    """Base I2C device class."""

    def __init__(self, addr, port=1):
        # type: (int, int) -> None
        """Initialization.

        :param addr: address of i2c device
        :param port: i2c bus: 0 - original Pi, 1 - Rev 2 Pi
        """
        self.addr = addr
        self.bus = smbus.SMBus(port)

    def write_byte(self, cmd):
        # type: (int) -> None
        """Write a single command."""
        self.bus.write_byte(self.addr, cmd)
        sleep(0.0001)

    def write_byte_data(self, cmd, data):
        # type: (int, int) -> None
        """Write a command and argument."""
        self.bus.write_byte_data(self.addr, cmd, data)
        sleep(0.0001)

    def write_block_data(self, cmd, data):
        # type: (int, int) -> None
        """Write a block of data."""
        self.bus.write_block_data(self.addr, cmd, data)
        sleep(0.0001)

    def read_byte(self):
        # type: () -> int
        """Read a single byte."""
        return self.bus.read_byte(self.addr)

    def read_byte_data(self, cmd):
        # type: (int) -> int
        """Read."""
        return self.bus.read_byte_data(self.addr, cmd)

    def read_block_data(self, cmd):
        # type: (int) -> int
        """Read a block of data."""
        return self.bus.read_block_data(self.addr, cmd)
