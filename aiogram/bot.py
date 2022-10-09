import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType
from random import randint
import sys
sys.path.append('../')
from telethon_bot_files import parse
from telethon_bot_files import spam

bot = Bot(token="")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
delay = 0
class States(StatesGroup):
    start = State()
    get_chat_link_for_username = State()
    get_chat_link_for_phone = State()
    get_chat_link_for_id = State()  
    wait_for_file = State()
    text_video = State()
    text_voice = State()
    text_picture = State()
    video = State()
    voice = State()
    picture = State()
    markup = State()
    textt = State()
    delay = State()
    
@dp.message_handler(state=States.textt)
async def spam_textt(message: types.Message):
    global delay
    await spam.start_spam1(message.text, None, delay, message)
    
@dp.message_handler(state=States.get_chat_link_for_username)
async def chat_link_for_username(message: types.Message, state: FSMContext):
    if "Парс " in message.text or "/start" in message.text or "http" not in message.text or "." not in message.text:
        await message.answser("Введите ссылку")
    else:
        await States.start.set()
        await message.answer("Парсинг начался . . .")
        file = open("../accounts.txt", "r")
        session = file.readline()
        await parse.start("username", message.text, session, message)
        
@dp.message_handler(state=States.get_chat_link_for_phone)
async def chat_link_for_usernamef(message: types.Message, state: FSMContext):
    if "Парс " in message.text or "/start" in message.text or "http" not in message.text or "." not in message.text:
        await message.answer("Введите ссылку")
    else:
        await States.start.set()
        await message.answer("Парсинг начался . . .")
        file = open("../accounts.txt", "r")
        session = file.readline()
        await parse.start("phone", message.text, session, message)
        
 
@dp.message_handler(state=States.get_chat_link_for_id)
async def chat_link_for_usernamef(message: types.Message, state: FSMContext):
    if "Парс " in message.text or "/start" in message.text or "http" not in message.text or "." not in message.text:
        await message.answer("Введите ссылку")
    else:
        await States.start.set()
        await message.answer("Парсинг начался . . .")
        file = open("../accounts.txt", "r")
        session = file.readline()
        await parse.start("id", message.text, session, message)
        

@dp.message_handler(state="*", commands=['start'])
async def start(message: types.Message):
    await States.start.set()
    username_btn = types.KeyboardButton("Парс")
    phones_btn = types.KeyboardButton("Рассылка")
    id_btn = types.KeyboardButton("Инвайтер")

    markup = types.ReplyKeyboardMarkup().add(username_btn, phones_btn).add(id_btn)
    await message.answer("Выберете нужное", reply_markup=markup)

@dp.message_handler(state="*")
async def buttons(message: types.Message):
    if message.text == "Парс":
        usernames = types.InlineKeyboardButton("Парс юзернеймов", callback_data="usernamepars")
        phones = types.InlineKeyboardButton("Парс номеров", callback_data="phonespars")
        ids = types.InlineKeyboardButton("Парс ID", callback_data="idspars")
        markup = types.InlineKeyboardMarkup().add(usernames).add(phones).add(ids)
        await message.answer("Выберете, что будем парсить:", reply_markup=markup)
    if message.text == "Рассылка":
        await message.answer("Отправьте файл парсинга usernames.txt")
        await States.wait_for_file.set()
        
@dp.message_handler(state=States.wait_for_file, content_types=[ContentType.DOCUMENT])
async def wait_for_file(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "../parse_res_from_user/usernames.txt")
    text = types.InlineKeyboardButton("Текст", callback_data="text")
    text_video = types.InlineKeyboardButton("Видео + текст", callback_data="textvideo")
    text_voice = types.InlineKeyboardButton("Аудио + текст", callback_data="textaudio")
    text_picture = types.InlineKeyboardButton("Фото + текст", callback_data="textpicture")
    video = types.InlineKeyboardButton("Видео", callback_data="video")
    voice = types.InlineKeyboardButton("Аудио", callback_data="audio")
    picture = types.InlineKeyboardButton("Фото", callback_data="picture")
    delay = types.InlineKeyboardButton("Задать задержку", callback_data="delay")
    markup = types.InlineKeyboardMarkup().add(text).add(text_video).add(text_voice).add(text_picture).add(video).add(voice).add(picture).add(delay)
    await message.answer("Выберете что будем рассылать:", reply_markup=markup)
    

@dp.callback_query_handler(state="*")
async def buttons(call: types.CallbackQuery):
    if call.data == "usernamepars":
        await States.get_chat_link_for_username.set()
        await call.message.answer("Отправьте ссылку на канал, откуда будем брать юзернеймы:")

    elif call.data == "phonespars":
        await States.get_chat_link_for_phone.set()
        await call.message.answer("Отправьте ссылку на канал, откуда будем брать номера:")
        
    elif call.data == "idspars":
        await States.get_chat_link_for_id.set()
        await call.message.answer("Отправьте ссылку на канал, откуда будем брать ID:")
        
    elif call.data == "text":
        await States.textt.set()
        await call.message.answer("Отправьте текст для рассылки")
        
        
    elif call.data == "textvideo":
        await States.text_video.set()
        await call.message.answer("Отправьте текст с видео в одном сообщении для рассылки")
        
        
    elif call.data == "textaudio":
        await States.text_voice.set()
        await call.message.answer("Отправьте текст с аудио в одном сообщении для рассылки")
        
        
    elif call.data == "textpicture":
        await States.text_picture.set()
        await call.message.answer("Отправьте текст с картинокой для рассылки")
        

    elif call.data == "video":
        await States.video.set()
        await call.message.answer("Отправьте видео для рассылки")
        

    elif call.data == "audio":
        await States.voice.set()
        await call.message.answer("Отправьте аудио для рассылки")
        

    elif call.data == "picture":
        await States.picture.set()
        await call.message.answer("Отправьте картинку для рассылки")
        
    elif call.data == "delay":
        delay5 = types.InlineKeyboardButton("0.08 мин.", callback_data="setdelay-5")
        delay60= types.InlineKeyboardButton("1 мин.", callback_data="setdelay-60")
        delay180 = types.InlineKeyboardButton("3 мин.", callback_data="setdelay-180")
        delay300 = types.InlineKeyboardButton("5 мин.", callback_data="setdelay-300")
        delay600 = types.InlineKeyboardButton("10 мин.", callback_data="setdelay-600")

        markup = types.InlineKeyboardMarkup().add(delay5).add(delay60).add(delay180).add(delay300).add(delay600) 
        await call.message.answer("Выберете задержку между спамом", reply_markup=markup)
    elif "setdelay" in call.data:
        global delay
        delay = int(call.data.split("-")[-1])
        await bot.answer_callback_query(call.id, "Задержка выставлена", show_alert=True)        
        await call.message.delete()
     
@dp.message_handler(state=States.text_picture, content_types=[ContentType.PHOTO, ContentType.TEXT])
async def spam_textpicture(message: types.Message):
    text = message.caption
    picture = await message.photo[-1].download('../user_src/picture.jpg')
    await States.start.set()
    global delay
    await spam.start_spam1(text, "picture.jpg", delay, message)
@dp.message_handler(state=States.text_voice, content_types=[ContentType.VOICE, ContentType.TEXT])
async def spam_textaudio(message: types.Message):
    text = message.caption
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "../user_src/voice.ogg")
    await States.start.set()
    global delay
    await spam.start_spam1(text, "voice.ogg", delay, message)

@dp.message_handler(state=States.text_video, content_types=[ContentType.TEXT, ContentType.VIDEO])
async def spam_textvideo(message: types.Message):
    text = message.caption
    file_id = message.video.file_id # Get file id
    file = await bot.get_file(file_id) # Get file path
    await bot.download_file(file.file_path, "../user_src/video.mp4")
    global delay
    await spam.start_spam1(text, "video.ogg", delay, message)

    await States.start.set()

@dp.message_handler(state=States.video, content_types=[ContentType.VIDEO])
async def spam_textvideo(message: types.Message):
    file_id = message.video.file_id # Get file id
    file = await bot.get_file(file_id) # Get file path
    await bot.download_file(file.file_path, "../user_src/video.mp4")
    await States.start.set()
    global delay
    await spam.start_spam1(None, "video.mp4", delay, message)


@dp.message_handler(state=States.picture, content_types=[ContentType.PHOTO])
async def spam_textvideo(message: types.Message):
    picture = await message.photo[-1].download('../user_src/picture.jpg')
    await States.start.set()
    global delay
    await spam.start_spam1(None, "picture.jpg", delay, message)

    
@dp.message_handler(state=States.voice, content_types=[ContentType.VOICE])
async def spam_textvideo(message: types.Message):
    text = message.caption
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "../user_src/voice.ogg")
    await States.start.set()
    global delay
    await spam.start_spam1(None, "voice.ogg", delay, message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
