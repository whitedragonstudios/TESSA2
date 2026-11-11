"""Find which MCP23017 pin each switch position uses. Run: python3 map_mcp_switch.py

Turn the switch to each position when asked, then press Enter. It prints the pin
that went low and, at the end, a SWITCH_PINS list for test_mcp23017.py.
Pin numbers: A0-A7 are 0-7, B0-B7 are 8-15. Keep the buttons released.
"""
import time
from adafruit_extended_bus import ExtendedI2C
from adafruit_mcp230xx.mcp23017 import MCP23017

BUS = 1
ADDR = 0x27

mcp = MCP23017(ExtendedI2C(BUS), address=ADDR)
mcp.iodir = 0xFFFF
mcp.gppu = 0xFFFF


def name(pin):
    return f"{'A' if pin < 8 else 'B'}{pin % 8}"


def low_pins():
    state = ~mcp.gpio & 0xFFFF
    return [p for p in range(16) if state >> p & 1]


found = []
for pos in range(1, 13):
    input(f"Turn the switch to position {pos}, then press Enter... ")
    time.sleep(0.2)
    pins = low_pins()
    print(f"  position {pos}: {[name(p) for p in pins] or 'none'}  (numbers {pins})")
    found.append(pins[0] if len(pins) == 1 else None)

print(f"\nSWITCH_PINS = {found}")
used = [p for p in found if p is not None]
print("Used twice:", sorted({p for p in used if used.count(p) > 1}) or "none")