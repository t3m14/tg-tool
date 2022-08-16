from telethon import TelegramClient
import asyncio
api_id = "14107984"
api_hash = "6507fadc1d76c1d8f3c0957690d9ec86"

async def main():
	apps = []
	file = open("accounts.txt", "r")
	lines = file.readlines()
	# итерация по строкам
	for line in lines:
		print(line.strip())

		apps.append(TelegramClient(str(line), api_id, api_hash))

	file.close()

	for app in apps:
		await app.start()

	for app in apps:
		await app.disconnect()

asyncio.run(main())