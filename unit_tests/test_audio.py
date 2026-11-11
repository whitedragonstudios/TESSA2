"""3.5mm jack to speaker with the volume encoder. Run: python3 test_audio.py"""
import math
import struct
import subprocess
import wave

DEVICE = "plughw:Headphones"   # the 3.5mm jack; None = system default (often HDMI)
RATE = 22050


def make_tone(path, seconds, left=True, right=True, freq=440):
    frames = bytearray()
    for n in range(int(RATE * seconds)):
        s = int(32767 * 0.4 * math.sin(2 * math.pi * freq * n / RATE))
        frames += struct.pack("<hh", s if left else 0, s if right else 0)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))


def play(path):
    cmd = ["aplay", "-q"] + (["-D", DEVICE] if DEVICE else []) + [path]
    subprocess.run(cmd, check=True)


make_tone("/tmp/left.wav", 1.5, right=False)
make_tone("/tmp/right.wav", 1.5, left=False)
make_tone("/tmp/steady.wav", 10)

print("Left channel tone"); play("/tmp/left.wav")
print("Right channel tone"); play("/tmp/right.wav")
print("Steady tone: turn the volume knob from min to max"); play("/tmp/steady.wav")