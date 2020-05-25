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

import util

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

def send_command(cmd):
    global game_bot_id, client

    try:
        client.send_message(game_bot, cmd)
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
