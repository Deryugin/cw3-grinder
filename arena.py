import datetime
import random
import time
from telethon import TelegramClient, sync
from enum import Enum

import telega, util, status

limit = False
wait_hr = -1
wait_day = -1

def arena_wait():
    util.log("Wait for arena finish..")
    for i in range(0,300):
        util.sleep(1)
        message = telega.last_msg()
        if 'Рейтинги обновлены:' in message.message:
            return
        if 'Даже драконы не могут' in message.message:
            return
        if 'Тебе бы подлечиться.' in message.message:
            return
        if 'У тебя нет денег, чтобы оплатить вход.' in message.message:
            return
    util.log("Arena waiting timeout!")

def arena_try():
    global limit
    global wait_hr
    global wait_day

    if status.get_money() < 5:
        return

    cur_day = int(datetime.datetime.utcnow().strftime('%d'))
    time = datetime.datetime.time(datetime.datetime.utcnow())

    # Check if arena was reset
    if time.hour == 10 and time.minute < 10 and cur_day != wait_day:
        limit = False
        wait_day = cur_day

    # If arena is over for today, do nothing
    if limit:
        return

    # Arena is closed for night
    if util.get_day_time(time) == util.day_time.NIGHT:
        return;

    # If we have no money, wait for next hour
    if wait_hr == time.hour:
        return

    util.sleep(random.randrange(0, 1200))
    telega.send_command('🗺Квесты');
    message = telega.last_msg()
    if '📯Арена 🔒' in message.message:
        limit = True
        return

    if message.button_count < 4:
        return

    telega.click(message, 4, "📯Арена")
    message = telega.last_msg()

    if 'Ты сейчас занят другим приключением' in message.message:
        util.sleep(300)
        return

    if not 'Пыльный воздух пропитан густым приторным' in message.message:
        return

    if '5/5' in message.message:
        # It's over for today
        limit = True
    else:
        for i in range(0, 5):
            util.sleep(5)
            telega.send_command('▶️Быстрый бой')
            arena_wait()
            message = telega.last_msg()
            hp = status.get_hp()
            if 'У тебя нет денег' in message.message or 'Тебе бы подлечиться.' in message.message or hp < 100:
                wait_hr = time.hour
                return
            if 'Даже драконы не могут' in message.message:
                limit = True
                return
