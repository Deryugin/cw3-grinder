#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2019, The ChatWars3 Grinder project
# License: GPL v3

import datetime
import random
import re
from time import sleep
from telethon import TelegramClient, sync
from enum import Enum
from parse import parse

import util
import telega
import pcp

force_upd = True
stamina = 0
mana = 0
money = 0
hp = 0 # from 0 to 100
last_stamina = datetime.datetime.now()
next_stamina = 0

has_target = False
force_target = True

def upd():
    util.log("Update")
    global stamina, force_upd, next_stamina, last_stamina, has_target, hp, mana, money
    force_upd = 0
    telega.send_command('🏅Герой')
    txt = telega.last_msg().message
    if not 'Состояние:' in txt:
        force_upd = 1
        return

    tmp = ""

    p = parse('{}выносливость: {}/{}', txt)
    if not p is None:
        stamina = int(p[1])

    p = parse('{}💧Мана: {}/{}', txt)
    if not p is None:
        mana = int(p[1])

    p = parse('{}💰{:d} {}', txt)
    if not p is None:
        money = int(p[1])

    p = parse('{}Здоровье: {:d}/{:d}{}', txt)
    if p is None:
        hp = 0
    else:
        hp = 100. * p[1] / p[2]

    p = parse('{}⏰{}мин{}', txt)
    if p is None:
        next_stamina = 1
    else:
        next_stamina = 1 + int(p[1])

    has_target = True
    if len(re.compile('Отдых').findall(txt)) > 0:
        has_target = False
    if len(re.compile('⚗️В лавке').findall(txt)) > 0:
        has_target = False

def get_stamina():
    util.log("Get stam")
    global stamina, force_upd, next_stamina, last_stamina
    now = datetime.datetime.now()
    if force_upd == True or ((now - last_stamina).seconds / 60) > next_stamina:
        upd()
        last_stamina = now
    util.log("Stamina: " + str(stamina) + "; next " + str(int(next_stamina - ((now - last_stamina).seconds / 60))))
    return stamina

def get_hp():
    global hp
    hp = 0
    upd()
    return hp

def get_mana():
    global mana
    return mana

def get_money():
    global money
    return money

def is_rest():
    global force_target
    now = datetime.datetime.now()
    if now.minute < 52 or force_target:
        upd()
        force_target = False

    util.log("Has_target = " + str(has_target))

    return not has_target

def send_report():
    m = telega.last_msg()
    if not 'Твои результаты в бою:' in m.message:
        print("Failed to send report")
        return

    dst = pcp.get("report_forward")
    if dst == "":
        print("Report destination is not configured")
        return
    if dst[0] != '@':
        dst = int(dst)
    m.forward_to(dst)

herb_by_name = { 'Stinky Sumac' : 39,
        'Mercy Sassafras' : 40,
        'Cliff Rue' : 41,
        'Love Creeper' : 42,
        'Wolf Root' : 43,
        'Swamp Lavender' : 44,
        'White Blossom' : 45,
        'Ilaves' : 46,
        'Ephijora' : 47,
        'Storm Hyssop' : 48,
        'Cave Garlic' : 49,
        'Yellow Seed' : 50,
        'Tecceagrass' : 51,
        'Spring Bay Leaf' : 52,
        'Ash Rosemary' : 53,
        'Sanguine Parsley' : 54,
        'Sun Tarragon' : 55,
        'Maccunut' : 56,
        'Dragon Seed' : 57,
        'Queen\'s Pepper' : 58,
        'Plasma of abyss' : 59,
        'Ultramarine dust' : 60,
        'Ethereal bone' : 61,
        'Itacory' : 62,
        'Assassin Vine' : 63,
        'Kloliarway' : 64,
        'Astrulic' : 65,
        'Flammia Nut' : 66,
        'Plexisop' : 67,
        'Mammoth Dill' : 68,
        'Silver dust' : 69 }

def get_herbs():
    telega.send_command('⚗️Алхимия')
    txt = telega.last_msg().message
    ret = {}
    for line in txt.split('\n'):
        res = parse('{} ({})', line)
        if res == None:
            continue
        code = herb_by_name[res[0]]
        ret[code] = int(res[1])

    return ret
