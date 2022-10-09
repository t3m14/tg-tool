from telethon import TelegramClient

API_ID = ""
API_KEY = ""
def login_by_session(session):
    client = TelegramClient(session, API_ID, API_KEY)
    return client
