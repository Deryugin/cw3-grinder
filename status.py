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
last_upd_txt = ""

is_aiming_var = False
has_target = False
force_target = True

def upd():
    telega.send_command('🏅Герой')
    util.log("Update")
    upd_from_txt(telega.last_msg().message)

def upd_from_txt(txt):
    global stamina, force_upd, next_stamina, last_stamina, has_target, hp, mana, money, last_upd_txt
    force_upd = 0
    if txt == last_upd_txt:
        return
    if not 'Битва семи замков через' in txt:
        return
    if not 'Состояние:' in txt:
        force_upd = 1
        return

    last_upd_txt = txt
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

    global is_aiming_var
    is_aiming_var = '🎯' in txt

def get_stamina(weak=False):
    util.log("Get stam")
    global stamina, force_upd, next_stamina, last_stamina
    now = datetime.datetime.now()
    if weak:
        util.log("Stamina weak update: " + str(stamina + (((now - last_stamina).seconds) / (60 * 60))))
        return stamina + ((now - last_stamina).seconds) / (60 * 60)
    if ((now - last_stamina).seconds / 60) > next_stamina + 1:
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

def is_aiming():
    global is_aiming_var
    return is_aiming_var

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

resource_by_name = {
        'Thread' : 1,
        'Stick' : 2,
        'Pelt' : 3,
        'Bone' : 4,
        'Coal' : 5,
        'Charcoal' : 6,
        'Powder' : 7,
        'Iron ore' : 8,
        'Cloth' : 9,
        'Silver ore' : 10,
        'Bauxite' : 11,
        'Cord' : 12,
        'Magic stone' : 13,
        'Wooden shaft' : 14,
        'Sapphire' : 15,
        'Solvent' : 16,
        'Ruby' : 17,
        'Hardener' : 18,
        'Steel' : 19,
        'Leather' : 20,
        'Bone powder' : 21,
        'String' : 22,
        'Coke' : 23,
        'Purified powder' : 24,
        'Silver alloy' : 25,
        'Steel mold' : 27,
        'Silver mold' : 28,
        'Blacksmith frame' : 29,
        'Artisan frame' : 30,
        'Rope' : 31,
        'Silver frame' : 32,
        'Metal plate' : 33,
        'Metallic fiber' : 34,
        'Crafted leather' : 35,
        'Quality Cloth' : 36,
        'Blacksmith mold' : 37,
        'Artisan mold' : 38,
        '💘Cupid\'s Essence' : 'e164',
}

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

def get_stock():
    telega.send_command('/inv')
    telega.send_command('📦Ресурсы')
    txt = telega.last_msg().message
    ret = {}
    for line in txt.split('\n'):
        if '/' in line:
            continue
        res = parse('{} ({})', line)
        if res == None:
            continue
        code = resource_by_name[res[0]]
        ret[code] = int(res[1])

    for line in txt.split('\n'):
        res = parse('/sg_{} {} ({})', line)
        if res == None:
            continue
        code = resource_by_name[res[1]]
        ret[code] = int(res[2])

    return ret

def stupid_human():
    h = pcp.get("human")
    if h == "":
        return False
    res = random.randrange(0, 100) < int(h)
    if res:
        util.log("Oh noes, I'm stoopid hooman :(")

    return res
