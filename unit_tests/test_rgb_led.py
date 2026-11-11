"""RGB LED (common cathode, software PWM). Run: python3 test_rgb_led.py"""
import time
from gpiozero import RGBLED

RED, GREEN, BLUE = 19, 16, 26   # BCM numbers

led = RGBLED(red=RED, green=GREEN, blue=BLUE)

for name, color in [("red", (1, 0, 0)), ("green", (0, 1, 0)),
                    ("blue", (0, 0, 1)), ("white", (1, 1, 1))]:
    print(f"LED should be {name}")
    led.color = color
    time.sleep(1.5)

print("Fading up and down")
for v in list(range(101)) + list(range(100, -1, -1)):
    led.color = (v / 100,) * 3
    time.sleep(0.02)

led.off()
print("LED should be off")
