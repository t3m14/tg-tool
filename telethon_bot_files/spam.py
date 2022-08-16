from .login import login_by_session
import random
import asyncio
import os

usernames_list = []
logins_list = []

def change_text(text):
    dic_to_change = {
    "о" : 'o',
    "О" : "0",
    "а" : "a",
    "А" : "A",
    "е" : "e",
    "Е" : "E",
    "З" : "3",
    "К" : "K",
    "В" : "B",
    "Т" : "T",
    "т" : "m",
    "Х" : "X",
    "х" : "X",
    "Н" : "H",
    "р" : "p",
    "Р" : "P",
    "М" : "M",
    }
    for i in text:
        is_change = random.randint(1, 2)
        if is_change == 1:
            try:
                text = text.replace(i, dic_to_change[i])
            except: pass
    return text

async def spam(client, usernames_list, text, document, delay, message):
    for username in usernames_list:
        print("Sending spam with text " + str(text) + " to username " + str(username))
        photo = open("../user_src/picture.jpg", "rb")
        voice = open("../user_src/voice.ogg", "rb")
        video = open("../user_src/video.mp4", "rb")
        print("Changing text ...")
        if text:
            text = change_text(text)
            #await message.answer("Текст изменён " + text)
        if document == None:
            await client.send_message(str(username), text)
        elif document.split(".")[-1] == "mp4":
            if text:
                await client.send_message(str(username), text, file=video)
            else:
                await client.send_message(str(username), file=voice, voice_note=True)
        elif document.split(".")[-1] == "ogg":
            if text:
                await client.send_message(str(username), text, file=voice, voice_note=True)
            else:
                await client.send_message(str(username), file=photo)
        elif str(document).split(".")[-1] == "jpg":
            if text:
                await client.send_message(str(username), text, file=photo)
            else:
                await client.send_message(str(username), file=photo)
        
        await message.answer("Сообщение было доставлено пользователю @" + str(username))
        await asyncio.sleep(delay)
        usernames_list.remove(username)

async def start_spam1(text, document, delay, message):
    print("ok")
    global usernames_list
    global logins_list
    file = open("../parse_res_from_user/usernames.txt", "r")
    lines = file.readlines()
    for line in lines:
        usernames_list.append(line.replace("\n", ""))
    file.close()
    for root, dirs, files in os.walk("../sessions"):
        for file in files:
            if(file.endswith(".session")):
                logins_list.append(file.split(".")[0])
    for l in logins_list:
        print(l)
        client = login_by_session(l)    
        try:
            await client.start()
        except:
            logins_list.remove(l)
        try:
            await spam(client, usernames_list, text, document, delay, message)
        except:
            logins_list.remove(l)
