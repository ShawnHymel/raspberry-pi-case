"""
Runs in the background and outputs some info on a tiny OLED screen

Hardware:
    128x32 OLED with SSD 1306 I2C controller
    https://www.amazon.com/dp/B079BN2J8V

Connections:
    GND - GND (pin 1)
    VCC - 3.3V (pin 9)
    SCL - SCL1 (pin 5)
    SDA - SDA1 (pin 3)

Before running this code, you must supply the API key from OctoPrint.
Log into OctoPrint via browser client, click Settings > Application Keys.
Create a new application, give it a name e.g. "oled-daemon" and copy the
API key that is presented to you. Paste that key into the API_KEY value
below.

Author: Shawn Hymel
Date: April 18, 2024
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

import requests
import socket
import fcntl
import struct
import time
from PIL import Image, ImageDraw, ImageFont

import board
from gpiozero import CPUTemperature
import adafruit_ssd1306

# Settings
API_KEY = "8D1F7E89763A4C6997675BA5285CD70E"
OLED_WIDTH = 128
OLED_HEIGHT = 32
OLED_ROTATION = 0       # 0: None, 1: 90°, 2: 180°, 3: 270°
OLED_I2C_ADDR = 0x3C    # I2C address of the OLED
OLED_REFRESH_SEC = 2.0  # How long to wait between display updates
NET_IFACE = "wlan0"     # Network interface for displaying IP address
OCTOPRINT_HOST = "http://localhost/"

#-------------------------------------------------------------------------------
# Functions

# Return the local IP address of the given interface
# https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-a-nic-network-interface-controller-in-python
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], "utf-8"))
    )[20:24])

# Return the CPU temperature
def get_cpu_temperature():
    return CPUTemperature().temperature

# Get print status
def get_octoprint_job_status():

    # Construct request
    url = requests.compat.urljoin(OCTOPRINT_HOST, "/api/job")
    headers = {"x-api-key": API_KEY}

    # Make request
    resp = requests.get(url, headers=headers)
    status = resp.json()

    return status

# Update display with status info
def update_oled_status(temperature, ip_addr, job_completion, job_time_left):
    img = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((0, 0), f"CPU Temp: {temperature}\N{DEGREE SIGN}C", font=font, fill=255)
    draw.text((0, 10), f"IP: {ip_addr}", font=font, fill=255)
    draw.text((0, 20), f"Job: {job_completion}", font=font, fill=255)
    draw.text((62, 20), f"Rem: {job_time_left}", font=font, fill=255)
    oled.image(img)
    oled.show()

#-------------------------------------------------------------------------------
# Main

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

# Main loop
while True:

    # Get IP address and CPU temperature
    ip_addr = get_ip_address(NET_IFACE)
    cpu_temperature = round(get_cpu_temperature(), 1)

    # Get job status from OctoPrint
    status = get_octoprint_job_status()
    job_completion = status["progress"]["completion"]
    job_time_left = status["progress"]["printTimeLeft"]

    # Convert status into strings
    if not job_completion:
        job_completion = "None"
        job_time_left = "000:00"
    else:
        job_completion = f"{round(job_completion)}%"
        hours = job_time_left // 60
        minutes = job_time_left % 60
        job_time_left = f"{hours:02d}:{minutes:02d}"

    # Write to OLED
    update_oled_status(cpu_temperature, ip_addr, job_completion, job_time_left)

    # Sleep for a bit
    time.sleep(OLED_REFRESH_SEC)
