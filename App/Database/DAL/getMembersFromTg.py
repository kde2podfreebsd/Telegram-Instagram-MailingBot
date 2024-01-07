from telethon import TelegramClient
from telethon import errors

api_id = 1
api_hash = ""
session_name = "test"
client = TelegramClient(session_name, api_id, api_hash)

async def getMembersFromTg(usernames, limit):
    async with client:
        db = []
        for username in usernames:
            try: 
                group_members = await client.get_participants(username, limit = limit)
                for member in group_members:
                    if (member.username):
                        db.append([member.first_name,
                        member.last_name,
                        member.username,
                        member.premium])
            except errors.rpcerrorlist.ChatAdminRequiredError: #нужны права админа, чтобы получить доступ к участникам
                pass
    return db 