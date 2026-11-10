"""MCP23017: 12-position switch + 4 buttons. Run: python3 test_mcp23017.py"""
import time
from adafruit_extended_bus import ExtendedI2C
from adafruit_mcp230xx.mcp23017 import MCP23017

BUS = 1
ADDR = 0x20
BUTTON_PINS = [12, 13, 14, 15]   # GPB4-7

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


for pos in range(1, 13):
    print(f"Turn the switch to position {pos}")
    ok = wait(lambda: active() & 0x0FFF == 1 << (pos - 1))
    print("  PASS" if ok else f"  FAIL (saw {active() & 0x0FFF:012b})")

for n, pin in enumerate(BUTTON_PINS, 1):
    print(f"Press and hold button {n}")
    ok = wait(lambda: active() & (1 << pin))
    print("  PASS" if ok else "  FAIL")
    wait(lambda: not active() & (1 << pin))
