from telethon import TelegramClient

API_ID = "14107984"
API_KEY = "6507fadc1d76c1d8f3c0957690d9ec86"
def login_by_session(session):
    client = TelegramClient(session, API_ID, API_KEY)
    return client