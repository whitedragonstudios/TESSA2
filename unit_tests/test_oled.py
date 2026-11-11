"""OLED screen (SSD1306 assumed). Run: python3 test_oled.py"""
import time
import adafruit_ssd1306
from adafruit_extended_bus import ExtendedI2C
from PIL import Image, ImageDraw

BUS = 5
ADDR = 0x3C
WIDTH, HEIGHT = 128, 64

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, ExtendedI2C(BUS), addr=ADDR)

oled.fill(1); oled.show()
print("All pixels should be on")
time.sleep(2)

oled.fill(0); oled.show()
print("All pixels should be off")
time.sleep(2)

img = Image.new("1", (WIDTH, HEIGHT))
ImageDraw.Draw(img).text((0, 0), "OLED OK", fill=255)
oled.image(img); oled.show()
print("Screen should say 'OLED OK'")
