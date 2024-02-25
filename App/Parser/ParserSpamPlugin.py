import asyncio
import uvloop

from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.DAL.ProxyDAL import ProxyAddressDAL
from App.Database.session import async_session
from App.Parser.InstagramParser import InstagramParser
from App.Config import UPDATE_DB_DELAY
import aioschedule

jobs = []

async def mainLayer():
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)
        proxy_dal = ProxyAddressDAL(session)
        uvloop.install()
        await update_followers_db(
            account_inst_dal=account_inst_dal
        )
        aioschedule.every(UPDATE_DB_DELAY).minutes.do(update_followers_db, account_inst_dal)

        await update_session_name_with_true_status(
            account_inst_dal=account_inst_dal
        )
        aioschedule.every().minute.do(update_session_name_with_true_status, account_inst_dal, proxy_dal)
        aioschedule.every().minute.do(spam_thread, account_inst_dal, proxy_dal)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)

async def spam_thread(account_inst_dal: AccountInstDAL, proxy_dal: ProxyAddressDAL):

    for job in aioschedule.jobs:
        tag = list(job.tags)
        if (tag not in accounts_session_names and tag != []):
            jobs.remove(
                find_client_and_delay_by_client_name(
                    client_name=tag[0]
                )
            )
            aioschedule.cancel_job(job)

    for account_name in accounts_session_names:
        account = await account_inst_dal.getAccountBySessionName(account_name)
        if account and account.target_channels:
            #delete job if its' delay has been changed 
            client_and_delay = check_if_delay_changed(client_name=account_name, delay=account.delay)
            if(client_and_delay):
                jobs.remove(client_and_delay)
                job_to_cancel = find_job_by_tag(client_name=account_name)
                aioschedule.cancel_job(job_to_cancel)

            #add job to jobs array if (it was not there or its' delay has been changed) and is in account_session_names
            if (
                    find_job_by_tag(client_name=account_name) is None 
                    and 
                    account_name in accounts_session_names
                ):
                jobs.append([account_name, account.delay])
                job = aioschedule.every(account.delay).minutes.do(
                    parser_thread, 
                    account_name, 
                    account.message, 
                    (None if account.reels_link == "Не указана" else account.reels_link),
                    account.id, 
                    proxy_dal
                )

                job.tags.add(f"{account_name}")

            

async def parser_thread(
        account_name: str, 
        message: str, 
        reels_link: str | None,
        id: int, 
        proxy_dal: ProxyAddressDAL
    ):
    tasks = []
    for follower in followers_db:
        proxies_list = await proxy_dal.getProxyAddressById(
            account_inst_id=id
        )
        if (follower["id"] == id):
            instagramParser = InstagramParser(
                login=account_name,
                password="",
                proxy=proxies_list[0]
            )
            proxies_list.append(proxies_list[0])
            proxies_list.remove(proxies_list[0])
            task = asyncio.create_task(
                instagramParser.async_send_message(message, reels_link, follower["username"])
            )
            tasks.append(task)
    await asyncio.gather(*tasks)

async def update_session_name_with_true_status(account_inst_dal: AccountInstDAL):
    global accounts_session_names
    accounts_session_names = await account_inst_dal.getSessionNamesWithTrueStatus()

async def update_followers_db(account_inst_dal: AccountInstDAL):
    global followers_db
    followers_db = await account_inst_dal.getAllFollowers()

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

