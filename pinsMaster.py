"""Barebones main file: pin declarations, imports and device setup for the Pi build.

Pin numbers for the Pi are BCM GPIO numbers (header pin in the comment).
MCP23017 pin numbers are 0-15: A0-A7 = 0-7, B0-B7 = 8-15.
Needs these lines in /boot/firmware/config.txt (then reboot):
    dtparam=i2c_arm=on
    dtoverlay=i2c3,pins_4_5
    dtoverlay=i2c4,pins_8_9
    dtoverlay=i2c5,pins_12_13
    dtoverlay=i2c6,pins_22_23
"""
import subprocess
import time

import adafruit_bme680
import adafruit_ssd1306
from adafruit_extended_bus import ExtendedI2C
from adafruit_mcp230xx.mcp23017 import MCP23017
from gpiozero import Button, RGBLED

# ------------------------------------------------------------------ settings

# MCP23017: 12-position switch and 4 buttons (I2C bus 1, header pins 3 and 5)
MCP_BUS = 1
MCP_ADDR = 0x27
SWITCH_PINS = [9, 8, 7, 6, 5, 4, 15, 14, 13, 12, 11, 10]   # MCP pin for position 1..12
BUTTON_PINS = [0, 1, 2, 3]                                  # MCP pin for buttons 1..4

# OLED screen, SSD1306 (I2C bus 5, header pins 32 and 33)
OLED_BUS = 5
OLED_ADDR = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 64

# BME688 sensor (I2C bus 4, header pins 24 and 21)
BME_BUS = 4
BME_ADDRS = (0x76, 0x77)

# HT16K33 boards driving the two 10-LED bars: name -> (I2C bus, address)
#   bar 1: bus 6, header pins 15 and 16     bar 2: bus 3, header pins 7 and 29
HT_BARS = {"bar1": (6, 0x70), "bar2": (3, 0x70)}
# (COM, ROW) for LED 1..10: all cathodes on COM0, LED n on ROW n
LED_MAP = [(0, row) for row in range(1, 11)]

# Toggle switches (BCM GPIO, other leg to GND): header pins 18 and 22
SWITCH_GPIOS = [24, 25]

# RGB LED, common cathode, software PWM: header pins 35, 36 and 37
RGB_GPIOS = {"red": 19, "green": 16, "blue": 26}

# Speaker: 3.5mm jack into the amp module
AUDIO_DEVICE = "plughw:Headphones"


# ------------------------------------------------------------------- devices

def setup_mcp():
    """Return the MCP23017 with every pin set as an input with a pull-up."""
    mcp = MCP23017(ExtendedI2C(MCP_BUS), address=MCP_ADDR)
    mcp.iodir = 0xFFFF
    mcp.gppu = 0xFFFF
    return mcp


def _low_pins(mcp, pins):
    state = ~mcp.gpio & 0xFFFF            # bit set = pin pulled low
    return [p for p in pins if state >> p & 1]


def read_switch_position(mcp):
    """Switch position 1-12, or None between detents."""
    low = _low_pins(mcp, SWITCH_PINS)
    return SWITCH_PINS.index(low[0]) + 1 if len(low) == 1 else None


def read_buttons(mcp):
    """List of 4 booleans, True while a button is pressed."""
    low = _low_pins(mcp, BUTTON_PINS)
    return [pin in low for pin in BUTTON_PINS]


def setup_oled():
    return adafruit_ssd1306.SSD1306_I2C(
        OLED_WIDTH, OLED_HEIGHT, ExtendedI2C(OLED_BUS), addr=OLED_ADDR)


def setup_bme():
    i2c = ExtendedI2C(BME_BUS)
    for addr in BME_ADDRS:
        try:
            return adafruit_bme680.Adafruit_BME680_I2C(i2c, address=addr)
        except (ValueError, OSError):
            continue
    raise RuntimeError(f"No BME688 at {[hex(a) for a in BME_ADDRS]} on bus {BME_BUS}")


class LedBar:
    """One HT16K33 board driving a 10-LED bar."""

    def __init__(self, bus, addr):
        self.i2c = ExtendedI2C(bus)
        self.addr = addr
        self._send([0x21])                # oscillator on
        self._send([0x81])                # display on
        self.set_brightness(15)
        self.clear()

    def _send(self, data):
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.addr, bytes(data))
        finally:
            self.i2c.unlock()

    def show(self, leds):
        """Light the given LEDs, numbered 1-10. Everything else is off."""
        ram = [0] * 16
        for n in leds:
            com, row = LED_MAP[n - 1]
            ram[2 * com + row // 8] |= 1 << (row % 8)
        self._send([0x00] + ram)

    def clear(self):
        self.show([])

    def set_brightness(self, level):
        """0 (dimmest) to 15 (brightest)."""
        self._send([0xE0 | max(0, min(15, level))])


def setup_bars():
    return {name: LedBar(bus, addr) for name, (bus, addr) in HT_BARS.items()}


def setup_switches():
    """Toggle switches; .is_pressed is True when a switch is ON."""
    return [Button(pin, pull_up=True) for pin in SWITCH_GPIOS]


def setup_rgb():
    """RGB LED; set .color = (r, g, b) with values 0-1."""
    return RGBLED(**RGB_GPIOS)


def play_sound(path):
    """Play a .wav file through the 3.5mm jack."""
    subprocess.run(["aplay", "-q", "-D", AUDIO_DEVICE, path], check=True)


# ---------------------------------------------------------------------- main

def main():
    mcp = setup_mcp()
    oled = setup_oled()
    bme = setup_bme()
    bars = setup_bars()
    switches = setup_switches()
    rgb = setup_rgb()
    print("All devices ready")

    while True:
        page = read_switch_position(mcp)          # 1-12, or None between detents
        buttons = read_buttons(mcp)               # [b1, b2, b3, b4]
        toggles = [s.is_pressed for s in switches]
        # temp, humidity, pressure, gas: bme.temperature, bme.relative_humidity,
        #                                bme.pressure, bme.gas
        # your program goes here
        time.sleep(0.05)


if __name__ == "__main__":
    main()