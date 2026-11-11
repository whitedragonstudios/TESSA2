"""MCP23017: 12-position switch + 4 buttons. Run: python3 test_mcp23017.py

Pin numbers: A0-A7 are 0-7, B0-B7 are 8-15.

This maps your wiring instead of assuming it. Part 1: turn the switch to each
position when asked and it prints which MCP pin went low. Part 2: press each
button when asked and it prints which pin went low. Keep buttons released
during Part 1 and the switch left alone during Part 2.
"""
import time
from adafruit_extended_bus import ExtendedI2C
from adafruit_mcp230xx.mcp23017 import MCP23017

BUS = 1
ADDR = 0x27
ALL_PINS = list(range(16))

i2c = ExtendedI2C(BUS)
mcp = MCP23017(i2c, address=ADDR)   # fails here if the chip does not answer
mcp.iodir = 0xFFFF                  # all inputs
mcp.gppu = 0xFFFF                   # pull-ups on
print(f"MCP23017 found at 0x{ADDR:02x}")


def name(pin):
    return f"{'A' if pin < 8 else 'B'}{pin % 8}"


def low_pins(exclude=()):
    state = ~mcp.gpio & 0xFFFF      # bit set = pin pulled low
    return [p for p in ALL_PINS if state >> p & 1 and p not in exclude]


def report(label, pins):
    if len(pins) == 1:
        print(f"  {label} -> {name(pins[0])}")
        return pins[0]
    print(f"  {label} -> FAIL, pins low: {[name(p) for p in pins] or 'none'}")
    return None


print("\n--- 12-position switch (buttons released) ---")
switch = []
for pos in range(1, 13):
    input(f"Turn the switch to position {pos}, then press Enter... ")
    time.sleep(0.2)
    switch.append(report(f"position {pos}", low_pins()))

print("\n--- Buttons (switch left in place; its pin is ignored) ---")
ignore = {p for p in switch if p is not None}
buttons = []
for n in range(1, 5):
    input(f"Press and HOLD button {n}, then press Enter... ")
    time.sleep(0.2)
    buttons.append(report(f"button {n}", low_pins(exclude=ignore)))

print(f"\nSWITCH_PINS = {switch}")
print(f"BUTTON_PINS = {buttons}")
used = [p for p in switch + buttons if p is not None]
print("Duplicates:", sorted({p for p in used if used.count(p) > 1}) or "none")
print("Unused pins:", [name(p) for p in ALL_PINS if p not in used] or "none")
