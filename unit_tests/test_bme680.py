"""BME688 sensor (uses the adafruit_bme680 driver). Run: python3 test_bme680.py"""
import time
import adafruit_bme680
from adafruit_extended_bus import ExtendedI2C

BUS = 4
ADDRS = (0x76, 0x77)   # 0x77 is the usual default; 0x76 when SDO is tied low

i2c = ExtendedI2C(BUS)
sensor = None
for addr in ADDRS:
    try:
        sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=addr)
        print(f"BME688 found at 0x{addr:02x}")
        break
    except (ValueError, OSError):
        print(f"nothing at 0x{addr:02x}")
    except RuntimeError as e:
        raise SystemExit(f"Chip answered at 0x{addr:02x} but the driver rejected it: {e}")

if sensor is None:
    raise SystemExit(f"No sensor at {[hex(a) for a in ADDRS]} on bus {BUS}. "
                     f"Try: i2cdetect -y {BUS}")

time.sleep(1)
for _ in range(3):
    print(f"temp {sensor.temperature:.1f} C  humidity {sensor.relative_humidity:.1f} %  "
          f"pressure {sensor.pressure:.1f} hPa  gas {sensor.gas} ohm")
    time.sleep(1)

ok = (-10 < sensor.temperature < 60 and 0 <= sensor.relative_humidity <= 100
      and 800 < sensor.pressure < 1100)
print("PASS" if ok else "FAIL: readings out of range")
