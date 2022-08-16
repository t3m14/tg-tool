from pyrogram import Client
API_ID = "14107984"
API_KEY = "6507fadc1d76c1d8f3c0957690d9ec86"
def login_by_session(session_file):
    app = Client(session_file, API_ID, API_KEY, workdir="../")
    return app
