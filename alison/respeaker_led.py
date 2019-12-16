"""
Control pixel ring on ReSpeaker 4 Mic Array
pip install pixel_ring gpiozero
"""

import time

from pixel_ring import pixel_ring
from gpiozero import LED

power = LED(5)
power.on()

pixel_ring.set_brightness(10)

def turn_on_led(R,G,B):
    try:
        pixel_ring.set_color(B,G,R)
        time.sleep(3)
        pixel_ring.off()
    except KeyboardInterrupt:
        print("bye")    















