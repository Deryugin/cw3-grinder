#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2020, The ChatWars3 Grinder project
# License: GPL v3

import string

def get(key):
    config_file = "config"
    f = open(config_file, "r")
    lines = f.readlines()
    f.close()

    for l in lines:
        key_pos = l.find("=")

        k = l[:key_pos]
        v = l[key_pos + 1:-1]

        if k == key:
            return v

    return ""
