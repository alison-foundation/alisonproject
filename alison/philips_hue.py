from phue import Bridge
import time
from collections import namedtuple
# import math
# import netifaces as ni

TIME_OUT = 2
XYPoint = namedtuple('XYPoint', ['x', 'y'])


def blink_led(r,g,b):   
    turn_on_alert(get_xy_point_from_rgb(r,g,b),3)

def turn_on_alert(value, nb):  # Turns on an alert

    # ni.ifaddresses('eth0')
    # ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    b = Bridge('192.168.1.100')
    b.connect()
    b.get_api()

    lights = b.get_light_objects()

    for light in lights:
        light.on = True
        light.brightness = 254
        light.xy = value

    i=0

    while i < nb :
        light.on = True;
        time.sleep(1)
        light.on = False
        time.sleep(1)
        i=i+1

    light.on = False



def turn_off_led(led_num):
    # ni.ifaddresses('eth0')
    # ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    b = Bridge('192.168.1.100')
    b.connect()
    b.get_api()

    b.set_light(led_num, 'on', False)
    time.sleep(TIME_OUT)


def turn_on_led(led_num):
    # ni.ifaddresses('eth0')
    # ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    b = Bridge('192.168.1.100')
    b.connect()
    b.get_api()

    b.set_light(led_num, 'on', True)
    time.sleep(TIME_OUT)


def set_xy_color(value):

    # ni.ifaddresses('eth0')
    # ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    b = Bridge('192.168.1.100')
    b.connect()
    b.get_api()
    lights = b.get_light_objects()

    for light in lights:
        light.on = True
        light.brightness = 254
        light.xy = value

    time.sleep(TIME_OUT)



def get_xy_point_from_rgb(red_i, green_i, blue_i):
    #"""Returns an XYPoint object containing the closest available CIE 1931 x, y coordinates
    #based on the RGB input values."""

    red = red_i / 255.0
    green = green_i / 255.0
    blue = blue_i / 255.0

    r = ((red + 0.055) / (1.0 + 0.055)) ** 2.4 if (red > 0.04045) else (red / 12.92)
    g = ((green + 0.055) / (1.0 + 0.055)) ** 2.4 if (green > 0.04045) else (green / 12.92)
    b = ((blue + 0.055) / (1.0 + 0.055)) ** 2.4 if (blue > 0.04045) else (blue / 12.92)

    X = r * 0.664511 + g * 0.154324 + b * 0.162028
    Y = r * 0.283881 + g * 0.668433 + b * 0.047685
    Z = r * 0.000088 + g * 0.072310 + b * 0.986039

    cx = X / (X + Y + Z)
    cy = Y / (X + Y + Z)

    # Check if the given XY value is within the colourreach of our lamps.
    xy_point = XYPoint(cx, cy)

    return xy_point

