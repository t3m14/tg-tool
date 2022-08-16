from pyrogram import Client, idle, enums
from .login import login_by_session
import asyncio


async def do_parse(app, chat_link, parse_obj, message):
   
    chat = await app.get_chat(chat_link)
    if parse_obj == "username":
        with open("../parse_results/usernames.txt", "w") as file:
            async for member in app.get_chat_members(chat.id, filter=enums.ChatMembersFilter.RECENT):
                user = member.user
                if user.username != None:
                    file.write(str(user.username)+"\n")
        to_send = open("../parse_results/usernames.txt", "rb")
        await message.answer_document(to_send)
    elif parse_obj == "phone":
        with open("../parse_results/phones.txt", "w") as file:
            async for member in app.get_chat_members(chat.id, filter=enums.ChatMembersFilter.RECENT):
                user = member.user
                if user.phone_number != None:
                    file.write(str(user.phone_number)+"\n")
        to_send = open("../parse_results/phones.txt", "rb")
        await message.answer_document(to_send)
    elif parse_obj == "id":
        with open("../parse_results/ids.txt", "w") as file:
            async for member in app.get_chat_members(chat.id, filter=enums.ChatMembersFilter.RECENT):
                user = member.user
                if user.id != None:
                    file.write(str(user.id)+"\n")
        to_send = open("../parse_results/ids.txt", "rb")
        await message.answer_document(to_send)

async def start_parse(session, chat_link, parse_obj, message):
    try:
        chat_link = chat_link.split("/")[-1]
    except:pass
    
    app = login_by_session(session)
    await app.start()
    await do_parse(app, chat_link, parse_obj, message)
    await app.stop()
