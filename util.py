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
def handle_outer_monsters():
    global last_known_msg
    src = pcp.get("monsters_source")
    m = telega.last_msg_uname(src)
    if m is None:
        return
    if m.message is None:
        return
    if m.message != last_known_msg:
        if last_known_msg != "" and "/fight_" in m.message:
            log("Helping monsters: " + m.message)
            m.forward_to('@ChatWarsBot')
        last_known_msg = m.message

last_self_msg = ""
def handle_self_monsters():
    global last_self_msg
    m = telega.last_msg()
    if m is None:
        return
    if m.message is None:
        return
    if m.message != last_self_msg and "/fight_" in m.message:
        log("Forwarding: " + m.message)
        dest = pcp.get("monsters_dest")
        if dest == "":
            return
        if dest[0] != '@':
            dest = int(dest)
        m.forward_to(dest)

        last_self_msg = m.message

def sleep(n):
    for i in range(0, n):
        handle_outer_monsters()
        handle_self_monsters()
        time.sleep(1)
