#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2019, The ChatWars3 Grinder project
# License: GPL v3

import datetime
import random
import time
from telethon import TelegramClient, sync
from enum import Enum
import pcp, telega

def timestamp(time):
    return (str(time.hour) + ":" + ("0" if time.minute < 10 else "") + str(time.minute) + ":" + ("0" if time.second < 10 else "") + str(time.second))

def log(msg):
    print (timestamp(datetime.datetime.time(datetime.datetime.now())) + "\t" + msg)

class day_time(Enum):
    NIGHT   = 1
    MORNING = 2
    DAY     = 3
    EVENING = 4

def get_day_time(time):
    t = (time.hour + 2) % 8
    if t < 2:
        return day_time.MORNING
    if t < 4:
        return day_time.DAY
    if t < 6:
        return day_time.EVENING
    return day_time.NIGHT

def is_number(str):
    try:
        int(str)
    except ValueError:
        return False
    else:
        return True

last_known_msg = ""
def handle_monsters():
    global last_known_msg
    src = pcp.get("monsters_forward")
    m = telega.last_msg_uname(src)
    if m is None:
        return
    if m.message != last_known_msg:
        if last_known_msg != "":
            m.forward_to('@ChatWarsBot')
        last_known_msg = m.message

def sleep(n):
    for i in range(0, n):
        handle_monsters()
        time.sleep(1)
