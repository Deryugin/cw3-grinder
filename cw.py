#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2019, The ChatWars3 Grinder project
# License: GPL v3

import datetime
import random
import pcp
from telethon import TelegramClient, sync
from enum import Enum

import telega, util, status, quest, arena

last_forest_hour = -1
last_msg_id = -1
quest_cmd = ['🌲Лес', '🍄Болото', '⛰️Долина']

time = datetime.datetime.time(datetime.datetime.utcnow())

telega.send_command('/report')
status.send_report()

while True:
    time = datetime.datetime.time(datetime.datetime.utcnow())

    message = telega.last_msg()
    if ('завывает по окрестным лугам' in message.message):
        util.log("Battle is not finished, wait 2 minutes")
        last_msg_id = message.id
        if time.minute < 8:
            util.sleep(60 * (8 - time.minute))
        else:
            util.sleep(120)
        telega.send_command('/report')
        status.send_report()
        continue

    message = telega.last_msg()
    if message.id != last_msg_id:
        last_msg_id = message.id
        util.log("Bot says: " + message.message)
        if 'Он пытается ограбить КОРОВАН' in message.message:
            if '/go' in message.message:
                telega.send_command('/go')
            else:
                message.click(0)
        elif not ('Кто знает' in message.message or 'драконы не могут драться' in message.message or 'отправился' in message.message or 'одолела' in message.message or 'сражение через' in message.message or 'занят другим' in message.message or 'Рейтинги обновлены: /top5 & /top6.' in message.message or 'Получено:' in message.message):
            util.log("Could not parse any key words")

    if (time.hour == 13 or time.hour == 21 or time.hour == 5) and time.minute >= 50:
        if status.is_rest() == True:
            def_target = pcp.get("def_target")
            if def_target == "guild":
                telega.send_command("/g_def")
            else:
                telega.send_command("🛡Защита")
            util.log("It's defense time! Wait for battle..")
        util.stash_resources()
        util.sleep(60 * (60 - time.minute + 8)) # Wait 8 minutes after battle so all stuff is calculated properly
        telega.send_command('/report')
        status.send_report()

    if not ((time.hour == 13 or time.hour == 21 or time.hour == 5) and time.minute >= 10):
        util.log("Try quests..")
        quest.run()

    arena.arena_try()

    util.transmute_try()

    message = telega.last_msg()

    if message.id != last_msg_id:
        last_msg_id = message.id
        util.log("Bot says: " + message.message)
        if 'Он пытается ограбить КОРОВАН' in message.message:
            if '/go' in message.message:
                telega.send_command('/go')
            else:
                message.click(0)

            util.log("Defend the KOPOBAH!")
        elif not ('Кто знает' in message.message or 'драконы не могут драться' in message.message or 'отправился' in message.message or 'одолела' in message.message or 'сражение через' in message.message or 'занят другим' in message.message or 'Рейтинги обновлены: /top5 & /top6.' in message.message or 'Получено:' in message.message):
            util.log("Could not parse any key words")

    util.sleep(30 + random.randrange(0,30))
