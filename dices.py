#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Denis Deryugin <deryugin.denis@gmail.com>
# Copyleft 2019, The ChatWars3 Grinder project
# License: GPL v3

import telega, util
from telethon import TelegramClient, sync
import random
from time import sleep

last_msg_id = 0

while True:
    telega.send_command("🎲Играть в кости")
    for i in range(0, 300):
        message = telega.last_msg()
        if '🎲Вы бросили кости на стол:' in message.message:
            sleep(random.randrange(0, 5))
            break
        sleep(1)
