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
from telethon.tl.custom import Message
from enum import Enum

import util, pcp, status

api_hash = pcp.get('api_hash')
api_id = pcp.get('api_id')

msg_limit = 20
client = TelegramClient('session_name', api_id, api_hash)
sleep(1)
client.start()
sleep(1)
game_bot = client.get_entity('ChatWarsBot')
game_bot_id = 265204902

auction_chan = client.get_entity('chatwars3')
#game_bot_id = 265204902

# Init global variables

def last_msg():
    global client

    try:
        idx = 0

        msgs = client.get_messages(game_bot, limit=msg_limit)

        while True:
            msg = msgs[idx]
            if msg.from_id == game_bot_id:
                status.upd_from_txt(msg.message)
                return msg
            idx = idx + 1

    except:
        util.log("Caught exception, return empty string") # wtf should be message type
        return Message(message="", id=0)

entity_dict = { }
def last_msg_uname(uname):
    global client
    global entity_dict

    if uname == "":
        return Message(message="", id=0)

    if uname[0] != '@':
        uname = int(uname)

    try:
        if not str(uname) in entity_dict:
            entity_dict[str(uname)] = client.get_entity(uname)

        msgs = client.get_messages(entity_dict[str(uname)], limit=1)
        return msgs[0]

    except:
        util.log("Caught exception, return empty string") # wtf should be message type
        return Message(message="", id=0)

def last_offer():
    global client

    try:
        idx = 0

        msgs = client.get_messages(auction_chan, limit=msg_limit)

        while True:
            msg = msgs[idx]
            return msg

    except:
        util.log("Caught exception, return empty string") # wtf should be message type
        return Message(message="", id=0)

def get_tentity(uname):
    global client
    global entity_dict

    if uname == "":
        return None

    if uname[0] != '@':
        uname = int(uname)

    if not str(uname) in entity_dict:
        entity_dict[str(uname)] = client.get_entity(uname)

    return entity_dict[str(uname)]

def send_msg(uname, text):
    global client
    global entity_dict

    if uname == "":
        return Message(message="", id=0)

    if uname[0] != '@':
        uname = int(uname)

    try:
        if not str(uname) in entity_dict:
            entity_dict[str(uname)] = client.get_entity(uname)

        client.send_message(entity_dict[str(uname)], text)
        return

    except:
        util.log("Caught exception, return empty string") # wtf should be message type
        return

def simmilar_chars(a, b):
    if ord(a) > ord(b):
        t = a
        a = b
        b = t
    # Latin first, cyrillic second
    if a == 'A' and b == 'А':
        return True
    if a == 'a' and b == 'а':
        return True
    if a == 'B' and b == 'В':
        return True
    if a == 'C' and b == 'С':
        return True
    if a == 'c' and b == 'с':
        return True
    if a == 'E' and b == 'е':
        return True
    if a == 'e' and b == 'е':
        return True
    if a == 'H' and b == 'Н':
        return True
    if a == 'K' and b == 'К':
        return True
    if a == 'M' and b == 'М':
        return True
    if a == 'O' and b == 'О':
        return True
    if a == 'o' and b == 'о':
        return True
    if a == 'P' and b == 'Р':
        return True
    if a == 'p' and b == 'р':
        return True
    if a == 'T' and b == 'Т':
        return True
    if a == 'X' and b == 'Х':
        return True
    if a == 'y' and b == 'у':
        return True
    return a == b

def button_fits(ctxt, btxt):
    if len(ctxt) != len(btxt):
        return False
    for i in range(0, len(ctxt)):
        if not simmilar_chars(ctxt[i], btxt[i]):
            return False

    return True

retries = 0
def send_command(cmd):
    global game_bot_id, client, retries

    try:
        if cmd[0] != '/':
            found = False
            back_found = False
            back_cmd = '⬅Назад'
            last = last_msg()
            if last.buttons is None:
                found = True
                print("No buttons -> no command sent! Try /me")
                sleep(3)
                send_command("/me")
                if cmd != "🏅Герой":
                    send_command(cmd)
                return

            for row in last.buttons:
                for button in row:
                    if button_fits(cmd, button.text):
                        found = True
                    if button_fits('⬅Назад', button.text):
                        back_found = True
                        back_cmd = button.text
            if found:
                retries = 0
            else:
                if retries > 2:
                    print("Fail for command ", cmd)
                    sys.exit()
                retries += 1
                if back_found:
                    send_command('⬅Назад')
                    send_command(cmd)
                else:
                    print("No such button: " + cmd)
                    send_command("/me")
                    if cmd != "🏅Герой":
                        send_command(cmd)
                return
            click(last, -1, cmd)
            return
        client.send_message(game_bot, cmd)
        if cmd != "/me":
            retry = 0
        util.log('Command is ' + cmd)
        for retry in range(0, 10):
            sleep(3)
            message = last_msg()
            if message.from_id == game_bot_id:
                return
        util.log("Command " + cmd + " answer timeout!")
    except:
        util.log("Fail..")

def click(message, idx, expected_text):
    print("Click text " + expected_text)
    cur_idx = 0
    if message.buttons is None:
        print("No buttons wtf #" + message.text + "#")
        return
    for row in message.buttons:
        for button in row:
            if button_fits(expected_text, button.text):
                if cur_idx != idx and idx >= 0:
                    print("Different index: ", cur_idx, ", expected ", idx)
                message.click(cur_idx)
                if expected_text != button.text:
                    print("Cheap shot: #"+expected_text+"#"+Button.text)
                sleep(3)
                return
            cur_idx += 1
    print("Button " + expected_text + " was not found")
