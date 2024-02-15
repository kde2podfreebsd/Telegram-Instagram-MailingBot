import asyncio
import uvloop
import aioschedule

from App.Database.DAL.AccountStoriesDAL import AccountStoriesDAL
from App.Database.session import async_session
from App.UserAgent.Core.UserAgentCore import UserAgentCore

jobs = []

async def mainLayer():
    async with async_session() as session:
        account_stories_dal = AccountStoriesDAL(session)
        uvloop.install()
        await update_premium_members_db(
            account_stories_dal=account_stories_dal
        )
        aioschedule.every().day.do(update_premium_members_db, account_stories_dal)

        global accounts_session_names_prev_state
        accounts_session_names_prev_state = await update_session_name_with_true_status(
            account_stories_dal=account_stories_dal
        )

        aioschedule.every().minute.do(update_session_name_with_true_status, account_stories_dal)
        aioschedule.every().minute.do(spam_plugin_thread, account_stories_dal)

        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)  

async def spam_plugin_thread(account_stories_dal: AccountStoriesDAL):
    user_agent_clients = [UserAgentCore(session_name) for session_name in accounts_session_names]

    # delete job if the account's status has been changed from True to False
    for job in aioschedule.jobs:
        tag = list(job.tags)
        print(tag)
        if (tag not in accounts_session_names and tag != []):
            jobs.remove(
                find_client_and_delay_by_client_name(
                    client_name=tag[0]
                )
            )
            aioschedule.cancel_job(job)

    for client in user_agent_clients:
        account = await account_stories_dal.getAccountBySessionName(session_name=client.session_name)
        if account and account.target_channels:
        
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
                job = aioschedule.every(account.delay).minutes.do(user_agent_thread, client, account.id)
                job.tags.add(f"{client.session_name}")

async def user_agent_thread(client: UserAgentCore, id: int):
    tasks = []
    premium_members = []
    for premium_member in premium_members_db:
        if (premium_member["id"] == id):
            premium_members.append(premium_member["username"])

    task = asyncio.create_task(client.giveReaction(premium_members))
    tasks.append(task)
    await asyncio.gather(*tasks)

async def update_session_name_with_true_status(account_stories_dal: AccountStoriesDAL):
    global accounts_session_names
    accounts_session_names = await account_stories_dal.getSessionNamesWithTrueStatus()

async def update_premium_members_db(account_stories_dal: AccountStoriesDAL):
    global premium_members_db
    premium_members_db = await account_stories_dal.getAllChatMembers()

    # нужно подумать над этим 
    # for job in aioschedule.jobs:
    #     aioschedule.cancel_job(job)

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