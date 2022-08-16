import time, os
from pyrogram import enums
from pyrogram.errors import PeerFlood
import random
import asyncio


def login(session_file):
    from pyrogram import Client
    API_ID = "14107984"
    API_KEY = "6507fadc1d76c1d8f3c0957690d9ec86"
    app = Client(session_file, API_ID, API_KEY, workdir="../")
    return app

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
    "к" : "k",
    "В" : "B",
    "Т" : "T",
    "Х" : "X",
    "х" : "X",
    "Н" : "H",
    "р" : "p",
    "Р" : "P",
    "М" : "M",
    "м" : "m"
    }
    for i in text:
        is_change = random.randint(1, 2)
        if is_change == 1:
            try:
                text = text.replace(i, dic_to_change[i])
            except: pass
    return text
        
async def spam(app, usernames_list, text, document, delay, message):
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
            await app.send_message(str(username), text=text)
        elif document.split(".")[-1] == "mp4":
            if text:
                app.send_video(str(username), video, caption=text)
            else:
                app.send_video(str(username), video)
        elif document.split(".")[-1] == "ogg":
            if text:
                app.send_voice(str(username), voice, caption=text)
            else:
                await app.send_voice(str(username), voice)
        elif str(document).split(".")[-1] == "jpg":
            if text:
                await app.send_photo(str(username), photo, caption=text)
            else:
                await app.send_photo(str(username), photo)
        
        await message.answer("Сообщение было доставлено пользователю @" + str(username))
        time.sleep(delay)
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
        app = login(l)    
        try:
            await app.start()
        except:
            logins_list.remove(l)
        try:
            await spam(app, usernames_list, text, document, delay, message)
        except:
            logins_list.remove(l)
