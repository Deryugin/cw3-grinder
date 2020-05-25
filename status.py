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

import util
import telega
import pcp

force_upd = True
stamina = 0
last_stamina = datetime.datetime.now()
next_stamina = 0

has_target = False
force_target = True

def upd():
    util.log("Update")
    global stamina, force_upd, next_stamina, last_stamina, has_target
    force_upd = 0
    telega.send_command('🏅Герой')
    txt = telega.last_msg().message
    if not 'Состояние:' in txt:
        force_upd = 1
        return

    tmp = ""

    p = re.compile('Выносливость: .*\/')
    L = p.findall(txt)
    tmp = L[0]
    util.log("look for stam in " + tmp)
    stamina = int(tmp[14:-1])
    p = re.compile('[0-9]+мин')
    L = p.findall(txt)
    if L:
        tmp = L[0]
        next_stamina = 1 + int(tmp[:-3])
    else:
        next_stamina = 1

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
    if not 'Твои результаты в бою:' in m.text:
        print("Failed to send report")
        return

    dst = pcp.get("report_forward")
    if dst == "":
        print("Report destination is not configured")
        return
    if dst[0] != '@':
        dst = int(dst)
    m.forward_to(dst)
