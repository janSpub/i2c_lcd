# i2c_lcd

## Description
i2c_lcd - module for control the 1-line/2-line LCD display via i2c interface.

## Requirements
* python 2/3
* `typing` package (for python 2 only)
* `smbus` package (usually pre-installed on the Raspberry PI):
    ```cmd
    sudo apt-get install i2c-tools
    sudo apt-get install python-smbus
    ```
* `smbus2` package - if you are using virtualenv without `--system-site-packages` flag (clean environment) 

## Installation
* pip install git+https://github.com/Azarko/i2c_lcd.git
* or clone + install 
    ```
    git clone git+https://github.com/Azarko/i2c_lcd.git
    pip install ./i2c_lcd
    ```

## Usage
### Module
```python
from i2c_lcd.lcd import I2CLcd
lcd = I2CLcd()
lcd.write('Hello world!')
lcd.set_cursor(line=2, position=1)
lcd.write('Line 2!')
```
### Entry-points
* `lcd-init` - initialize the LCD. Must use on first run or after power reset.
* `lcd-display-ip` - a small sample, show current local IP of your PC.
* `lcd-backlight [on/off]` - switch LCD backlight.
* `lcd-write "text" --line num` - write `text` on the line `num`. 
If line not selected - write on the first line. The display won't be cleared before starting.
* `lcd-clear` - clear the LCD.
