import asyncio
import random

import uvloop

from App.Config import singleton
from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Database.session import async_session
from App.UserAgent.Core.UserAgentCore import UserAgentCore
import aioschedule

@singleton
class MessageTracker:
    def __init__(self):
        self.message_ids = {}

    def record_message(self, session_name, chat, message_id):
        if session_name not in self.message_ids:
            self.message_ids[session_name] = {}
        self.message_ids[session_name][chat] = message_id

    def get_last_message_id(self, session_name, chat):
        return self.message_ids.get(session_name, {}).get(chat, None)

    def clear_last_message_id(self, session_name, chat):
        if session_name in self.message_ids and chat in self.message_ids[session_name]:
            del self.message_ids[session_name][chat]

message_tracker = MessageTracker()
jobs = []

async def mainLayer():
    async with async_session() as session:
        account_dal = AccountDAL(session)

        uvloop.install()

        await update_session_name_with_true_status(account_dal=account_dal)

        aioschedule.every().minute.do(update_session_name_with_true_status, account_dal)
        aioschedule.every().minute.do(spam_plugin_thread, account_dal)

        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)  

async def spam_plugin_thread(account_dal: AccountDAL):
    user_agent_clients = [UserAgentCore(account_name) for account_name in accounts_session_names]

    for job in aioschedule.jobs:
        tag = list(job.tags)
        if (tag not in accounts_session_names and tag != []):
            jobs.remove(
                find_client_and_delay_by_client_name(
                    client_name=tag[0]
                )
            )
            aioschedule.cancel_job(job)

    for client in user_agent_clients:
        account = await account_dal.getAccountBySessionName(session_name=client.session_name)
        if account and account.advertising_channels:
        
            #delete job if its' delay has been changed 
            client_and_delay = check_if_delay_changed(client_name=client.session_name, delay=account.delay)
            if(client_and_delay):
                jobs.remove(client_and_delay)
                job_to_cancel = find_job_by_tag(client_name=client.session_name)
                aioschedule.cancel_job(job_to_cancel)

            #add job to jobs array if (it was not there or its' delay has been changed) and is in account_session_names
            if (
                    find_job_by_tag(client_name=client.session_name) is None 
                    and 
                    client.session_name in accounts_session_names
                ):
                jobs.append([client.session_name, account.delay])
                job = aioschedule.every(account.delay).seconds.do(
                    user_agent_thread, client, account.advertising_channels, message_tracker, account.message
                )
                job.tags.add(f"{client.session_name}")         
    
async def user_agent_thread(
        client: UserAgentCore, 
        advertising_channels: list,
        message_tracker: MessageTracker,
        message: str
    ):
    for chats in advertising_channels:
        last_message_id = message_tracker.get_last_message_id(client.session_name, chats)
        if last_message_id:
            await client.deleteMsg(chat=chats, message_ids=last_message_id)
            message_tracker.clear_last_message_id(client.session_name, chats)

        msg = await client.sendMsg(chat=chats, message=message)
        message_tracker.record_message(client.session_name, chats, msg['msg_ids'])

async def update_session_name_with_true_status(account_dal: AccountDAL):
    global accounts_session_names
    accounts_session_names = await account_dal.getSessionNamesWithTrueStatus()

def find_client_and_delay_by_client_name(client_name: str):
    result = None
    for job in jobs:
        if (job[0] == client_name):
            result = job
    return result

def check_if_delay_changed(client_name: str, delay: int):
    result = None
    new_job = [client_name, delay]
    for job in jobs:
        if ((job[0] == new_job[0]) and (job[1] != new_job[1])):
            result = job
    return result 

def find_job_by_tag(client_name: str):
    result = None
    for job in aioschedule.jobs:
        if (client_name in job.tags):
            result = job
    return result

if __name__ == "__main__":
    asyncio.run(mainLayer())
