"""Two HT16K33 boards driving the 10-segment LED bars. Run: python3 test_ht16k33_bars.py

LED_MAP gives (COM, ROW) for each of the 10 LEDs. Default is the shared-row
layout: LEDs 1-5 on COM0, LEDs 6-10 on COM1, ROW0-4.
For one LED per ROW (all on COM0) use: LED_MAP = [(0, r) for r in range(10)]
"""
import time
from adafruit_extended_bus import ExtendedI2C

BARS = {5: 0x70, 6: 0x70}   # I2C bus -> address
LED_MAP = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
           (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]


def send(i2c, addr, data):
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(addr, bytes(data))
    finally:
        i2c.unlock()


def show(i2c, addr, leds):
    ram = [0] * 16
    for i in leds:
        com, row = LED_MAP[i]
        ram[2 * com + row // 8] |= 1 << (row % 8)
    send(i2c, addr, [0x00] + ram)


for bus, addr in BARS.items():
    i2c = ExtendedI2C(bus)
    send(i2c, addr, [0x21])   # oscillator on
    send(i2c, addr, [0x81])   # display on
    send(i2c, addr, [0xEF])   # full brightness

    print(f"Bar on bus {bus}: all 10 LEDs on")
    show(i2c, addr, range(10))
    time.sleep(2)

    print(f"Bar on bus {bus}: one LED at a time, 1 to 10")
    for i in range(10):
        show(i2c, addr, [i])
        time.sleep(0.3)

    show(i2c, addr, [])
print("Done. Both bars should be off.")
