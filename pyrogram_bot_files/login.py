from pyrogram import Client
API_ID = ""
API_KEY = ""
def login_by_session(session_file):
    app = Client(session_file, API_ID, API_KEY, workdir="../")
    return app
