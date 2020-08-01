import datetime
import random
from telethon import TelegramClient, sync
from enum import Enum

import telega, util, status, pcp

def is_number(str):
    try:
        int(str)
    except ValueError:
        return False
    else:
        return True

def req_stam(lines):
    res = 0
    for c in lines:
        if len(c) == 0:
            continue

        w = c.split(" ")
        if is_number(w[0]):
            if w[1][0] == 'k':
                res = res + 2 * int(w[0])
            else:
                res = res + int(w[0])

    save_stam = pcp.get('save_stam')
    if save_stam == '':
        return res
    else:
        return res + int(save_stam)

def day_time_ok(lines):
    res = []
    if 'morning' in lines[0]:
        res += [util.day_time.MORNING]
    if 'day' in lines[0]:
        res += [util.day_time.DAY]
    if 'evening' in lines[0]:
        res += [util.day_time.EVENING]
    if 'night' in lines[0]:
        res += [util.day_time.NIGHT]

    if len(res) == 0:
        res = [util.day_time.MORNING, util.day_time.DAY, util.day_time.EVENING, util.day_time.NIGHT]

    time = datetime.datetime.time(datetime.datetime.utcnow())
    if util.get_day_time(time) in res:
        return True
    else:
        return False

quest_cmd = ['🌲Лес', '🍄Болото', '⛰️Долина', '🗡ГРАБИТЬ КОРОВАНЫ']
wait_hr = -1
def run():
    global wait_hr
    global time

    time = datetime.datetime.time(datetime.datetime.utcnow())
    if wait_hr != -1:
        if time.hour > wait_hr:
            wait_hr = -1
        else:
            return

    iterator = 0
    qrange = 1
    fp = open('quest')
    lines = fp.read().split("\n")
    fp.close()

    stamina = status.get_stamina(weak=True)

    print("Required stamina points: " + str(req_stam(lines)) + ", got " + str(stamina))

    if stamina < req_stam(lines):
        return

    if not day_time_ok(lines):
        print("Bad day time")
        return
    #if util.get_day_time(time) == util.day_time.NIGHT: # or get_day_time(time) == day_time.EVENING:
    #    telega.send_command('/on_tch')
    #    qrange = 4
    stamina = status.get_stamina(weak=False)
    if stamina < req_stam(lines):
        return
    for i in lines:
        if len(i) == 0:
            continue

        util.log("Iterator = " + i)

        if i[0] == '/':
            if not status.stupid_human():
                telega.send_command(i)
            continue

        telega.send_command('🗺Квесты')

        q_message = telega.last_msg()
        w = i.split(" ")
        q = ""
        if is_number(w[0]):
            q_idx = 0
            if w[1][0] == 's':
                q_idx = 1
            elif w[1][0] == 'm':
                q_idx = 2
            elif w[1][0] == 'k':
                q_idx = 3

            if q_message.button_count < q_idx:
                return
            q = quest_cmd[q_idx]

            for it in range(0, int(w[0])):
                if w[1][0] == 'r':
                    q_idx = random.randrange(0, 3)
                expected_text = "🌲Лес"
                if q_idx == 1:
                    expected_text = "🍄Болото"
                elif q_idx == 2:
                    expected_text = "🏔Долина"
                else:
                    expected_text = "🗡ГРАБИТЬ КОРОВАНЫ"
                telega.click(q_message. q_idx, expected_text)
                message = telega.last_msg()

                last_msg_id = message.id
                if '4' in message.message:
                    util.log("Wait 4 min..")
                    util.sleep(4 * 60 + random.randrange(15, 60))
                elif '5' in message.message:
                    util.log("Wait 5 min..")
                    util.sleep(5 * 60 + random.randrange(15, 60))
                elif '6' in message.message:
                    util.log("Wait 6 min..")
                    util.sleep(6 * 60 + random.randrange(15, 60))
                elif '7' in message.message:
                    util.log("Wait 7 min..")
                    util.sleep(7 * 60 + random.randrange(15, 60))
                elif '8' in message.message:
                    util.log("Wait 8 min..")
                    util.sleep(8 * 60 + random.randrange(15, 60))
                elif 'Тебе бы подлечиться.' in message.message:
                    wait_hr = time.hour
                    return
                else:
                    util.log("Strange forest time: " + message.message);
                    util.log("Try to wait 5 mins anyway")
                    util.sleep(5 * 60)
            if status.stupid_human():
                return

            message = telega.last_msg()

            if 'И свой факел' in message.message: # Craft a new torch
                telega.send_command('/bind_tch')
                telega.send_command('/on_tch')

            if 'Он пытается ограбить КОРОВАН' in message.message:
                if '/go' in message.message:
                    telega.send_command('/go')
                else:
                    if message.button_count > 0:
                        message.click(0)

    status.stamina = 0

    #status.force_upd = True

def go_def():
    if status.stupid_human():
        return
    if status.is_rest() == True:
        def_target = pcp.get("def_target")
        if def_target == "guild":
            telega.send_command("/g_def")
        elif def_target == "alliance":
            telega.send_command("/ga_def")
        else:
            telega.send_command("🛡Защита")
        util.log("It's defense time! Go to sleep..")
