"""MCP23017: 12-position switch + 4 buttons. Run: python3 test_mcp23017.py

Pin numbers: A0-A7 are 0-7, B0-B7 are 8-15.
SWITCH_PINS is the MCP pin for switch position 1, 2, 3 ... 12 in order.
BUTTON_PINS is assumed to be the four pins the switch does not use: A0-A3.
Edit either list if your wiring differs.
"""
import time
from adafruit_extended_bus import ExtendedI2C
from adafruit_mcp230xx.mcp23017 import MCP23017

BUS = 1
ADDR = 0x27
SWITCH_PINS = [9, 8, 7, 6, 5, 4, 15, 14, 13, 12, 11, 10]
BUTTON_PINS = [0, 1, 2, 3]

i2c = ExtendedI2C(BUS)
mcp = MCP23017(i2c, address=ADDR)   # fails here if the chip does not answer
mcp.iodir = 0xFFFF                  # all inputs
mcp.gppu = 0xFFFF                   # pull-ups on
print(f"MCP23017 found at 0x{ADDR:02x}")


def name(pin):
    return f"{'A' if pin < 8 else 'B'}{pin % 8}"


def low_pins(candidates):
    state = ~mcp.gpio & 0xFFFF      # bit set = pin pulled low
    return [p for p in candidates if state >> p & 1]


def wait(cond, secs=15):
    end = time.time() + secs
    while time.time() < end:
        if cond():
            return True
        time.sleep(0.02)
    return False


print("\n--- 12-position switch ---")
for pos, pin in enumerate(SWITCH_PINS, 1):
    print(f"Turn the switch to position {pos} (expect {name(pin)})")
    ok = wait(lambda: low_pins(SWITCH_PINS) == [pin])
    if ok:
        print("  PASS")
    else:
        seen = [name(p) for p in low_pins(SWITCH_PINS)] or "none"
        print(f"  FAIL (saw {seen})")

print("\n--- Buttons ---")
for n, pin in enumerate(BUTTON_PINS, 1):
    print(f"Press and hold button {n} (expect {name(pin)})")
    ok = wait(lambda: pin in low_pins(BUTTON_PINS))
    if ok:
        print("  PASS")
    else:
        seen = [name(p) for p in range(16) if p not in SWITCH_PINS and p in low_pins(range(16))] or "none"
        print(f"  FAIL (other pins low: {seen})")
    wait(lambda: pin not in low_pins(BUTTON_PINS))