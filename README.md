# i2c_lcd

## Description
i2c_lcd - module for controlling 1-line/2-line LCD display via i2c interface.

## Requirements
* python 2/3
* `smbus` package (usually pre-installed on the Raspberry PI):
  ```cmd
  sudo apt-get install i2c-tools
  sudo apt-get install python-smbus
  ```

## Installation
* `pip install git+https://github.com/Azarko/i2c_lcd.git`
* or clone + install 
  ```
  git clone https://github.com/Azarko/i2c_lcd.git
  pip install ./i2c_lcd
  ```

## Usage

### Module
The most common methods:
* `clear()` - clear LCD and return cursor to original position if shifted (left edge on first line of the display);
* `return_home()` - return cursor to original position if shifted (left edge on first line of the display);
* `set_cursor(line, position)` - change cursor position to selected (default line=1, position=1);
* `write(string)` - display string or letter on lcd (at current cursor position);
* `set_backlight(True/False)` - change lcd back light;
* `shift_cursor(left=False)` - shift cursor to selected direction;
* `shift_display(left=False)` - shift display to selected direction. Cursor follows the display shift;

Methods for configure:
* `set_shift_mode(display=False, reverse=False)` - set cursor/display shift mode. Also set direction of move/shift;
* `set_display(display=True, cursor=False, blink=False)` - set display parameters;
* `enable_display()` - enable display mode. In this mode characters and cursor (if enabled) are shown on the LCD.
It is not a backlight! It is an alias for `set_display`;
* `disable_display()` - disable display mode. In this mode characters and cursor aren't shown on the LCD.
It is not a backlight! It is an alias for `set_display`;
* `enable_cursor()` - enable cursor displaying mode. In this mode cursor (_) is shown on the LCD. Can be displayed 
along with blink (`enable_blink`). It is an alias for `set_display`;
* `disable_cursor()` - disable cursor displaying mode. In this mode cursor (_) isn't shown on the LCD. It is an alias 
for `set_display`;
* `enable_blink()` - enable blink displaying mode. In this mode blink is shown on the LCD. Can be displayed along with 
cursor (`enable_cursor`). It is an alias for `set_display`;
* `disable_blink()` - disable blink displaying mode. In this mode blink isn't shown on the LCD. It is an alias for 
`set_display`;
* `enable_shift_display()` - shift the display while writing on the LCD. The cursor is fixed:
  ```
  lcd.enable_shift_display()
  lcd.write(' a')
  | |a|_| | |
  lcd.write('b')
  |a|b|_| | |
  ```
  This is an alias for `set_shift_mode`;
* `enable_shift_cursor()` - shift the cursor while writing on the LCD. The display is fixed:
  ```
  lcd.enable_shift_cursor()
  lcd.write(' a')
  | |a|_| | |
  lcd.write('b')
  | |a|b|_| |
  ```
  This is an alias for `set_shift_mode`;
* `enable_reverse()` - set reverse direction mode for writing (right to left). This is an alias for `set_shift_mode`;
* `disable_reverse()` - set default direction mode for writing (left to right). This is an alias for `set_shift_mode`;

Sample of usage:
```python
import time
from i2c_lcd import I2CLcd
lcd = I2CLcd()
lcd.write('Hello world!')
lcd.set_cursor(line=2, position=1)
lcd.write('Line 2!')
time.sleep(5)
lcd.clear()
```

```python
from i2c_lcd import display_ip
display_ip()    # detect and display ip-address
```

### Entry-points
If the package is installed via `pip` there are several commands available
for use:
* `lcd-init` - initialize the LCD. Must be used at first run or after power
reset;
* `lcd-display-ip` - a small sample, show current local IP of your PC;
* `lcd-backlight [on/off]` - switch LCD backlight;
* `lcd-write "text" --line num` - write `text` on the line `num`;
If line is not selected - write on the first line. The display won't be
cleared automatically before writing;
* `lcd-clear` - clear the LCD.
