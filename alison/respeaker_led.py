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

def boot():
    turn_on_led(255,0,0, 1)
    turn_on_led(0,255,0, 1)
    turn_on_led(0,0,255, 1)
    pixel_ring.off()

def turn_on_led(R,G,B,delay):
    try:
        pixel_ring.set_color(B,R,G)
        time.sleep(delay)
        pixel_ring.off()
    except KeyboardInterrupt:
        print("bye")    

def blink(R, G, B, nbr=3):
    for i in range(nbr):
        turn_on_led(R,G,B, 0.5)
        pixel_ring.off()
        time.sleep(0.5)
#boot()
blink(255,0,0, 6)













