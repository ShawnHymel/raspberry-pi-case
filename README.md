# Case and scripts for OctoPrint on Raspberry Pi

## Case

Case designed for Raspberry Pi 3B in FreeCAD.

## Scripts

### oled-daemon.py

Controls OLED connected to I2C on Raspberry Pi. Hardware: https://www.amazon.com/gp/product/B079BN2J8V/

Run as service in the background (TODO: write service file).

### shutter.sh

Toggles a GPIO pin on the Raspberry Pi to manually control a Canon DSLR shutter. Install the OctoLapse plugin. Create a new "camera" profile and set this as the "External Camera Script."

## License

Case design: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en)

Scripts: [0BSD](https://opensource.org/license/0bsd)
