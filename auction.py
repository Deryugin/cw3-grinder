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

def init_cost(txt):
    for s in txt.split("\n"):
        if not 'price' in s:
            continue

        for q in s.split(" "):
            if util.is_number(q):
                return int(q)

        break

    return 9999

while True:
    offer = telega.last_offer()
    txt = offer.message
    bet = txt.split("\n")[-1]
    if offer.id != last_msg_id:
        bf = open('bids')
        for i in bf.read().split("\n"):
            first_s = i.find(' ')
            if first_s < 1 or len(i[first_s + 1:]) == 0 or not util.is_number(i[:first_s]):
                if len(i) > 0:
                    print("Wrong format for bid: " + i)
                continue

            if i[first_s + 1:] in txt and init_cost(i) <= int(i[:first_s]):
                sleep(random.randrange(1, 15))
                telega.send_command(bet + "_" + i[:first_s])
        bf.close()

    if last_msg_id != offer.id:
        print("New offer: " + bet + "; " + txt.split("\n")[1])

    last_msg_id = offer.id
    sleep(1)
