"""Two toggle switches on Pi GPIOs (other leg to GND). Run: python3 test_switches.py"""
import time
from gpiozero import Button

PINS = [17, 27]   # BCM numbers

for n, pin in enumerate(PINS, 1):
    sw = Button(pin, pull_up=True)
    print(f"Flip switch {n} ON")
    t = time.time()
    while not sw.is_pressed and time.time() - t < 15:
        time.sleep(0.02)
    print("  PASS" if sw.is_pressed else "  FAIL")
    print(f"Flip switch {n} OFF")
    t = time.time()
    while sw.is_pressed and time.time() - t < 15:
        time.sleep(0.02)
    print("  PASS" if not sw.is_pressed else "  FAIL")
    sw.close()
