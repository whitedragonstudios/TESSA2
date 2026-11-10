"""MCP23017: 12-position switch + 4 buttons. Run: python3 test_mcp23017.py

Pin numbers: A0-A7 are 0-7, B0-B7 are 8-15.
SWITCH_PINS lists the MCP pin for switch position 1, 2, 3 ... 12 in order.
If your positions are wired in a different order, edit that list.
"""
import time
from adafruit_extended_bus import ExtendedI2C
from adafruit_mcp230xx.mcp23017 import MCP23017

BUS = 1
ADDR = 0x27
SWITCH_PINS = [8, 9, 10, 11, 12, 13, 14, 15,   # positions 1-8  -> B0-B7
               0, 1, 2, 3]                     # positions 9-12 -> A0-A3
BUTTON_PINS = [4, 5, 6, 7]                     # buttons 1-4    -> A4-A7

i2c = ExtendedI2C(BUS)
mcp = MCP23017(i2c, address=ADDR)   # fails here if the chip does not answer
mcp.iodir = 0xFFFF                  # all inputs
mcp.gppu = 0xFFFF                   # pull-ups on
print(f"MCP23017 found at 0x{ADDR:02x}")


def active():
    return ~mcp.gpio & 0xFFFF       # bit set = pin pulled low


def wait(cond, secs=15):
    end = time.time() + secs
    while time.time() < end:
        if cond():
            return True
        time.sleep(0.02)
    return False


switch_mask = sum(1 << p for p in SWITCH_PINS)

for pos, pin in enumerate(SWITCH_PINS, 1):
    print(f"Turn the switch to position {pos}")
    ok = wait(lambda: active() & switch_mask == 1 << pin)
    print("  PASS" if ok else f"  FAIL (saw pins {[p for p in range(16) if active() >> p & 1]})")

for n, pin in enumerate(BUTTON_PINS, 1):
    print(f"Press and hold button {n}")
    ok = wait(lambda: active() & (1 << pin))
    print("  PASS" if ok else "  FAIL")
    wait(lambda: not active() & (1 << pin))