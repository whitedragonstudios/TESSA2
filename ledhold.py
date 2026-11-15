"""Hold one LED on for 60 seconds so you can look at it or probe it with a meter.
Run: python3 led_hold.py

ROW is the HT16K33 ROW pin the LED's anode (through its resistor) is wired to.
If you move the wire to a different, reachable ROW pin, change ROW here.
"""
import time
from adafruit_extended_bus import ExtendedI2C

BUS, ADDR = 6, 0x70   # HT16K33 #1 (use BUS = 3 for #2)
ROW = 4               # LED 4 is on ROW4
COM = 0               # all cathodes are on COM0

i2c = ExtendedI2C(BUS)


def send(data):
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(ADDR, bytes(data))
    finally:
        i2c.unlock()


send([0x21])   # oscillator on
send([0x81])   # display on
send([0xEF])   # full brightness

ram = [0] * 16
ram[2 * COM + ROW // 8] |= 1 << (ROW % 8)
send([0x00] + ram)
print(f"ROW{ROW} on COM{COM} is on for 60 s. Press Ctrl+C to stop early.")
try:
    time.sleep(60)
finally:
    send([0x00] + [0] * 16)
    print("off")