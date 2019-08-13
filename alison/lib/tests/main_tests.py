#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             : Alison Foundation
# Date created       : 13 August 2019
# Date last modified : 13 August 2019
# Python Version     : 3.*

"""
    This is the main entry point for automated build tests
"""

class Tests(object):
    """docstring for Tests."""

    def __init__(self, log=False):
        super(Tests, self).__init__()
        self.log    = log
        self.header = " Running tests ".center(70,"=")

    def run(self, log=False):
        """Starts the tests"""
        log = log or self.log # To activate logging
        print(self.header)
        # Here you can put your tests, a few examples :
        self.test("Basic true assertion", 1 == 1, True)
        self.test("Are mathematical laws respected ?", 2 + 2, 4)
        self.test("Basic false assertion", 1 == 1, False)
        # End of the tests
        print("==> Test Campaign done.")
        return None

    def test(self, testname, result, expected):
        """Documentation for test"""
        outcome = False
        print("  - "+testname[:45].ljust(45), end="")
        try:
            assert(result == expected)
        except Exception as e:
            print("\x1b[1m[\x1b[91mFAILED\x1b[0m\x1b[1m]\x1b[0m")
            outcome = False
        else:
            print("\x1b[1m[\x1b[92mPASSED\x1b[0m\x1b[1m]\x1b[0m")
            outcome = False
        return outcome


if __name__ == '__main__':
    t = Tests()
    t.run()
