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
import pcp, telega, status

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

last_known_location = ""
def handle_hidden_location():
    global last_known_location

    m = telega.last_msg()
    if m is None:
        return

    if m.message is None:
        return

    if not "То remember the route you associated it with simple combination:" in m.message:
        return

    if m.message == last_known_location:
        return

    last_known_location = m.message

    dst = pcp.get("location_dst")
    if dst == "":
        return

    m.forward_to(dst)

last_known_msg = ""
def handle_outer_monsters():
    global last_known_msg
    src = pcp.get("monsters_source")
    m = telega.last_msg_uname(src)
    if m is None:
        return
    if m.message is None:
        return
    if m.message == last_known_msg:
        return

    if last_known_msg == "" or not "/fight_" in m.message:
        last_known_msg = m.message
        return

    last_known_msg = m.message

    log("Helping monsters: " + m.message)
    fhp = pcp.get("fight_hp")
    if fhp != "" and int(fhp) > status.get_hp():
        log("Low hp: " + str(status.get_hp()))
        return

    if status.get_stamina() < 1:
        log("No stamina")
        return

    m.forward_to('@ChatWarsBot')

    sleep(2)

    if 'Ты собрался напасть на врага' in telega.last_msg().message:
        target_chat = pcp.get("monsters_ack_dest")
        telega.send_msg(target_chat, "+")

    if "⚜️Forbidden Champion" in m.message and pcp.get("champ_pots") == "true":
        telega.send_command("/use_p03")
        telega.send_command("/use_p02")
        telega.send_command("/use_p01")
        telega.send_command("/use_p06")
        telega.send_command("/use_p05")
        telega.send_command("/use_p04")

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
        if (i % 10) == 0:
            handle_hidden_location()
            handle_outer_monsters()
            handle_self_monsters()
        time.sleep(1)
