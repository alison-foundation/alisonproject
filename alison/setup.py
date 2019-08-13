#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : setup.py
# Author             : Alison Foundation
# Date created       : 13 August 2019
# Date last modified : 13 August 2019
# Python Version     : 3.*

from setuptools import setup

import lib.core.AppInfos as i

setup(
    name         = i.get_name(),
    version      = i.get_version(),
    description  = i.get_description(),
    url          = i.get_url(),
    author       = i.get_author(),
    author_email = i.get_author_email(),
    license      = 'GPL3',
    packages     = [
        'alison',
        'alison/lib/core',
        'alison/lib/'
    ],
    zip_safe     = False
)
