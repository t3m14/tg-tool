from .login import login_by_session
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import re

async def dump_all_participants(channel, parse_func, client, message):
	offset_user = 0    # номер участника, с которого начинается считывание
	limit_user = 100   # максимальное число записей, передаваемых за один раз

	all_participants = []   # список всех участников канала
	filter_user = ChannelParticipantsSearch('')

	while True:
		participants = await client(GetParticipantsRequest(channel,
			filter_user, offset_user, limit_user, hash=0))
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset_user += len(participants.users)


	all_users_details = []   # список словарей с интересующими параметрами участников канала

	for participant in all_participants:
		all_users_details.append({"id": participant.id,
			"first_name": participant.first_name,
			"last_name": participant.last_name,
			"user": participant.username,
			"phone": participant.phone,
			"is_bot": participant.bot})
	print(all_users_details)
	if parse_func == "phone":
		with open("../parse_results/phones.txt", 'w') as file:
			await message.answer("Парсинг телефонов")
			for user in all_users_details:
				if user["phone"] != None:
					file.write(str(user["phone"])+"\n")
	elif parse_func == "id":
		with open("../parse_results/ids.txt", 'w') as file:
			await message.answer("Парсинг айди")
			for user in all_users_details:
				if user["id"] != None:
					file.write(str(user["id"])+"\n")
	elif parse_func == "username":
		with open("../parse_results/usernames.txt", 'w') as file:
			await message.answer("Парсинг юзренеймов")
			for user in all_users_details:
				if user["user"] != None:
					file.write(user["user"]+"\n")
	to_send = open(f"../parse_results/{parse_func}s.txt", "rb")
	await message.answer_document(to_send)	
 
async def start(parse_func, channel, session, message):
	print("OKK")
	client = login_by_session(session)	
	async with client:
		print("OKK 2")
		client.loop.run_until_complete(await dump_all_participants(channel, parse_func, client, message))
