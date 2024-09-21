"""
Displays some test strings on 3 rows of the OLED screen.

Hardware:
    128x32 OLED with SSD 1306 I2C controller
    https://www.amazon.com/dp/B079BN2J8V

Connections:
    GND - GND (pin 9)
    VCC - 3.3V (pin 1)
    SCL - SCL1 (pin 5)
    SDA - SDA1 (pin 3)

Author: Shawn Hymel
Date: September 21, 2024
License: 0BSD (https://opensource.org/license/0bsd)

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE
FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY
DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import time
from PIL import Image, ImageDraw, ImageFont

import board
from gpiozero import CPUTemperature
import adafruit_ssd1306

# Settings
OLED_WIDTH = 128
OLED_HEIGHT = 32
OLED_ROTATION = 0       # 0: None, 1: 90°, 2: 180°, 3: 270°
OLED_I2C_ADDR = 0x3C    # I2C address of the OLED

# Define OLED
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(
    OLED_WIDTH,
    OLED_HEIGHT,
    i2c,
    addr=OLED_I2C_ADDR
)
oled.rotation = OLED_ROTATION

# Clear the display
oled.fill(0)
oled.show()

# Draw some text on the OLED
img = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()
draw.text((0, 0), "This is a test", font=font, fill=255)
draw.text((0, 10), "Test on another row", font=font, fill=255)
draw.text((0, 10), "Test on a third row", font=font, fill=255)
oled.image(img)
oled.show()

# Wait before exiting
time.sleep(5.0)
