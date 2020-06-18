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
    hp = status.get_hp()
    if fhp != "" and int(fhp) > hp:
        log("Low hp: " + str(hp))
        return

    if status.get_stamina() < 1:
        log("No stamina")
        return

    m.forward_to(telega.game_bot)

    time.sleep(2)

    if 'Ты собрался напасть на врага' in telega.last_msg().message:
        target_chat = pcp.get("monsters_ack_dest")
        telega.send_msg(target_chat, "+ ❤️" + str(int(hp)) + "%hp")

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

last_bar_msg = ""
def handle_bartrender():
    global last_bar_msg
    src = pcp.get("bartrender_chat")
    if src == "":
        return
    m = telega.last_msg_uname(src)
    if m is None:
        return
    if m.message is None:
        return
    if m.message == last_bar_msg:
        return

    if last_bar_msg == "" or \
            not "/g_withdraw" in m.message or \
            (not " p0" in m.message and \
            not " p1" in m.message and \
            not " p2" in m.message):
        last_bar_msg = m.message
        return

    last_bar_msg = m.message

    log("Doing bartrender stuff: " + m.message)

    m.forward_to(telega.game_bot)

    time.sleep(2)

    last = telega.last_msg()
    if 'Withdrawing' in last.message:
        last.forward_to(telega.get_tentity(src))

def sleep(n):
    while n >= 0:
        t1 = time.time()
        if (n % 10) == 0:
            handle_hidden_location()
            handle_outer_monsters()
            handle_self_monsters()
            handle_bartrender()
        time.sleep(1)
        t2 = time.time()
        n = n - int(t2 - t1)

def try_buy(code, max_cost):
    telega.send_command("/t_"+str(code))
    amount = int(status.get_money() / max_cost)
    if 'по ' + str(amount) + '💰' in telega.last_msg().message:
        if amount == 0:
            return
        telega.send_command("/wtb_"+str(code)+"_"+str(amount))

def transmute_try():
    trm_from = pcp.get("trm_from")
    trm_to = pcp.get("trm_to")
    trm_mana = pcp.get("trm_mana")

    if trm_from == '' or trm_to == '' or trm_mana == '':
        return

    if status.get_mana() < int(trm_mana):
        return

    herbs = status.get_herbs()

    force_upd = False
    do_trm = True
    for h in trm_from.split(','):
        h = int(h)
        if (h == 0) or not h in herbs:
            continue

        if do_trm and herbs[h] >= 50 and status.get_mana() > int(trm_mana):
            force_upd = True
            trm_cmd = '/use_trm ' + str(h) + ' ' + trm_to
            telega.send_command(trm_cmd)
            if '[Недостаточно маны]' in telega.last_msg().message:
                do_trm = False


        if random.random() < 0.1:
            try_buy(h, 1)

    if force_upd:
        status.upd()
