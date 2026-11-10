"""BME680 sensor. Run: python3 test_bme680.py"""
import time
import adafruit_bme680
from adafruit_extended_bus import ExtendedI2C

BUS = 4
ADDR = 0x76   # use 0x77 if SDO is tied high

sensor = adafruit_bme680.Adafruit_BME680_I2C(ExtendedI2C(BUS), address=ADDR)
time.sleep(1)

for _ in range(3):
    print(f"temp {sensor.temperature:.1f} C  humidity {sensor.relative_humidity:.1f} %  "
          f"pressure {sensor.pressure:.1f} hPa  gas {sensor.gas} ohm")
    time.sleep(1)

ok = (-10 < sensor.temperature < 60 and 0 <= sensor.relative_humidity <= 100
      and 800 < sensor.pressure < 1100)
print("PASS" if ok else "FAIL: readings out of range")
