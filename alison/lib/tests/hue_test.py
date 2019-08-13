#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             : Alison Foundation
# Date created       : 13 August 2019
# Date last modified : 13 August 2019
# Python Version     : 3.*

from philips_hue import *

def main():
    try:
        print("Testing mode 1\n")
        turn_on_alert(2, 1)

        print("Testing mode 2\n")
        turn_on_alert(2, 2)

        print("Testing mode 3\n")
        turn_on_alert(2, 3)

        print("Testing mode 4\n")
        turn_on_alert(2, 4)

    except KeyboardInterrupt:
        turn_off_led(2)


if __name__ == '__main__':
    main()
