#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2019, The ChatWars3 Grinder project
# License: GPL v3

import datetime
import random
import pcp
import time
import sys
from telethon import TelegramClient, sync
from enum import Enum

import telega, util, status, quest, arena

last_forest_hour = -1
last_msg_id = -1
quest_cmd = ['🌲Лес', '🍄Болото', '⛰️Долина']

now = datetime.datetime.time(datetime.datetime.utcnow())

#if not status.stupid_human():
#    telega.send_command('/report')
#    status.send_report()
status.upd()

while True:
    now = datetime.datetime.time(datetime.datetime.utcnow())

    if pcp.get("night_mode") != "":
        h = int(pcp.get("night_mode"))
        if now.hour == h:
            time.sleep(random.randrange(0, 1200))
            quest.go_def()
            time.sleep(8 * 60 * 60 + random.randrange(0, 1200))
    message = telega.last_msg()
    if ('завывает по окрестным лугам' in message.message):
        util.log("Battle is not finished, wait 2 minutes")
        last_msg_id = message.id
        if now.minute < 8:
            util.sleep(60 * (8 - now.minute))
        else:
            util.sleep(120)
        if not status.stupid_human():
            telega.send_command('/report')
            status.send_report()
        continue

    message = telega.last_msg()
    if message.id != last_msg_id:
        last_msg_id = message.id
        util.log("Bot says: " + message.message)
        if 'Он пытается ограбить КОРОВАН' in message.message:
            if status.stupid_human():
                time.sleep(300)
                continue
            if '/go' in message.message:
                telega.send_command('/go')
            else:
                telega.click(message, 0, "🧹Вмешаться")
        elif 'To accept their offer, you shall /pledge to protect.' in message.message:
            telega.send_command('/pledge')
        elif not ('Кто знает' in message.message or 'драконы не могут драться' in message.message or 'отправился' in message.message or 'одолела' in message.message or 'сражение через' in message.message or 'занят другим' in message.message or 'Рейтинги обновлены: /top5 & /top6.' in message.message or 'Получено:' in message.message):
            util.log("Could not parse any key words")

    if (now.hour == 13 or now.hour == 21 or now.hour == 5) and now.minute >= 30:
        if status.is_rest() == True:
            time.sleep(random.randrange(0, 1200))
            quest.go_def()
            util.log("It's defense time! Wait for battle..")
        util.stash_resources()
        util.sleep(60 * (60 - now.minute + 8)) # Wait 8 minutes after battle so all stuff is calculated properly
        if not status.stupid_human():
            telega.send_command('/report')
            status.send_report()

    if not ((now.hour == 13 or now.hour == 21 or now.hour == 5) and now.minute >= 10):
        util.log("Try quests..")
        quest.run()

    arena.arena_try()

    util.transmute_try()

    message = telega.last_msg()

    if message.id != last_msg_id:
        last_msg_id = message.id
        util.log("Bot says: " + message.message)
        if 'Он пытается ограбить КОРОВАН' in message.message:
            if status.stupid_human():
                time.sleep(600)
                continue
            if '/go' in message.message:
                telega.send_command('/go')
            else:
                telega.click(message, 0, "🧹Вмешаться")

            util.log("Defend the KOPOBAH!")
        elif 'To accept their offer, you shall /pledge to protect.' in message.message:
            telega.send_command('/pledge')
        elif not ('Кто знает' in message.message or 'драконы не могут драться' in message.message or 'отправился' in message.message or 'одолела' in message.message or 'сражение через' in message.message or 'занят другим' in message.message or 'Рейтинги обновлены: /top5 & /top6.' in message.message or 'Получено:' in message.message):
            util.log("Could not parse any key words")

    util.sleep(30 + random.randrange(0,30))
