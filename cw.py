#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2019, The ChatWars3 Grinder project
# License: GPL v3

import datetime
import random
from time import sleep
from telethon import TelegramClient, sync
from enum import Enum

import telega, util, status, quest

last_forest_hour = -1
last_msg_id = -1
quest_cmd = ['🌲Лес', '🍄Болото', '⛰️Долина']

time = datetime.datetime.time(datetime.datetime.utcnow())

while True:
    time = datetime.datetime.time(datetime.datetime.utcnow())

    message = telega.last_msg()
    if ('завывает по окрестным лугам' in message.message):
        telega.send_command('/report')
        util.log("Battle is not finished, wait 2 minutes")
        last_msg_id = message.id
        if time.minute < 8:
            sleep(60 * (8 - time.minute))
        else:
            sleep(120)
        continue

    message = telega.last_msg()
    if message.id != last_msg_id:
        last_msg_id = message.id
        util.log("Bot says: " + message.message)
        if 'нажми /go' in message.message:
            telega.send_command('/go')
            util.log("defend the kopobah!")
        elif not ('Кто знает' in message.message or 'драконы не могут драться' in message.message or 'отправился' in message.message or 'одолела' in message.message or 'сражение через' in message.message or 'занят другим' in message.message or 'Рейтинги обновлены: /top5 & /top6.' in message.message or 'Получено:' in message.message):
            util.log("Could not parse any key words")

    if (time.hour == 13 or time.hour == 21 or time.hour == 5) and time.minute >= 50 and status.is_rest() == True:
        telega.send_command('/g_def')
        util.log("It's defense time! Wait for battle..")
        sleep((60 - time.minute + 8) * 60) # Wait 8 minutes after battle so all stuff is calculated properly
        telega.send_command('/report')

    if not ((time.hour == 13 or time.hour == 21 or time.hour == 5) and time.minute >= 10):
        util.log("Try quests..")
        quest.run()

    message = telega.last_msg()

    if message.id != last_msg_id:
        last_msg_id = message.id
        util.log("Bot says: " + message.message)
        if '/go' in message.message:
            telega.send_command('/go')
            util.log("Defend the KOPOBAH!")
        elif not ('Кто знает' in message.message or 'драконы не могут драться' in message.message or 'отправился' in message.message or 'одолела' in message.message or 'сражение через' in message.message or 'занят другим' in message.message or 'Рейтинги обновлены: /top5 & /top6.' in message.message or 'Получено:' in message.message):
            util.log("Could not parse any key words")

    sleep(30 + random.randrange(0,30))
