import asyncio
import uvloop
import os 
import sys
import io
import subprocess

from telethon import TelegramClient
import telethon.tl.functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon import functions
from telethon import types

from App.Config import sessions_dirPath
from App.Config import basedir
from App.Logger import ApplicationLogger

logger = ApplicationLogger()


class UserAgentCore:
    def __init__(self, session_name: str):
        self.session_name = session_name
        self.app = TelegramClient(f"{sessions_dirPath}/{session_name}", api_id=123, api_hash="123")

        logger.log_info(
            f"Init UserAgentCore on {session_name} session. Path to session {sessions_dirPath}/{session_name}"
        )

    @classmethod
    @logger.exception_handler
    async def createSession(cls, session_name: str, api_id: int, api_hash: str):
        async with TelegramClient(
            f"{sessions_dirPath}/{session_name}", api_id, api_hash
        ) as app:
            await app.send_message("me", f"init session {session_name}")
            logger.log_info(
                f"Create session {session_name} in path: {sessions_dirPath}/{session_name}"
            )

    @logger.exception_handler
    async def sendMsg(
        self,
        chat: str | int,
        message: str,
        parseMode='md',
    ):
        async with self.app as app:
            output = await app.send_message(
                chat, message, parse_mode=parseMode
            )
            logger.log_info(f"Send message to: {chat}. Message: {message}")
            return {"msg_ids": output.id, "chat": chat}

    @logger.exception_handler
    async def deleteMsg(self, chat: str | int, message_ids: int):
        async with self.app as app:
            chat_entity = await self.app.get_entity(chat)
            await app.delete_messages(entity=chat_entity, message_ids=message_ids)
            logger.log_info(f"Deleted message from: {chat}. Message: {message_ids}")

    @logger.exception_handler
    async def joinChat(self, chat: str | int):
        async with self.app as app:
            chat_entity = await self.app.get_entity(chat)
            await app.join_chat(chat_entity)
            logger.log_info(f"Join in chat: {chat}")

    @logger.exception_handler
    async def leaveChat(self, chat: str | int):
        async with self.app as app:
            await app.leave_chat(chat)
            logger.log_info(f"Leave from chat: {chat}")

    @logger.exception_handler
    async def getMe(self):
        async with self.app as app:
            logger.log_info(
                f"Get info about account registered by {self.session_name} session"
            )
            return await app.get_me()
    
    @logger.exception_handler
    async def editFirstName(self, new_first_name):
        async with self.app as app:
            await app(telethon.tl.functions.account.UpdateProfileRequest(
                first_name=new_first_name
            ))
            logger.log_info(
                f"{self.session_name}'s first name has been changed to {new_first_name}"
            )

    @logger.exception_handler
    async def editLastName(self, new_last_name):
        async with self.app as app:
            await app(telethon.tl.functions.account.UpdateProfileRequest(
                last_name=new_last_name
            ))
            logger.log_info(
                f"{self.session_name}'s last name has been changed to {new_last_name}"
            )
    
    @logger.exception_handler
    async def editUsername(self, new_username):
        async with self.app as app:
            await app(telethon.tl.functions.account.UpdateUsernameRequest(
                username=new_username
            ))
            logger.log_info(
                f"{self.session_name}'s username has been changed to {new_username}"
            )
    
    @logger.exception_handler
    async def changeProfilePicture(self, file_content):
        with open("temp_photo.jpg", "wb") as temp_file:
            temp_file.write(file_content)

        async with self.app as app:
            file_result = await app.upload_file("temp_photo.jpg")
            await app(telethon.tl.functions.photos.UploadProfilePhotoRequest(
                file=file_result
            ))
            logger.log_info(
                f"{self.session_name}'s profile picture has been changed"
            )
            os.remove("temp_photo.jpg")
    
    @logger.exception_handler
    async def changeProfileDescription(self, new_account_description):
        async with self.app as app:
            print("pfp desc CHANGED: ", new_account_description)
            await app(
                UpdateProfileRequest(
                    about=new_account_description
                )
            )
            logger.log_info(f"{self.session_name}'s profile description has been changed to {new_account_description}")
    
    async def getProfilePictures(self, entity):
        async with self.app as app:
            photos = await app.get_profile_photos(entity)
            return photos 
    
    async def getProfileBio(self, entity):
        async with self.app as app:
            full = await app(GetFullUserRequest(entity))
            return full.full_user.about 
    
    async def getProfilePictureId(self):
        async with self.app as app:
            entity = await self.getMe()
            pfps = await self.getProfilePictures(entity)
            photo_id = pfps[0].id
            return photo_id
        
    async def downloadProfilePhoto(self):
        async with self.app as app:
            file_name = await app.download_profile_photo("me", file='me.jpg')
            link = f"/Users/user/Spam-Tg-Inst-Service/{file_name}"
            return link 
    
    async def uploadPhoto(self, link):
        async with self.app as app:
            file = await app.upload_file(link)
            return file

    @logger.exception_handler
    async def giveReaction(self, usernames):
        async with self.app as app:

            max_ids = await self.getAllPeerMaxIDsRequest(
                usernames=usernames
            )
            stories_watched = 0
            for username, max_id in zip(usernames, max_ids):
                if (max_id != 0):
                    stories_watched += 1
                    await app(functions.stories.ReadStoriesRequest(
                        peer=username,
                        max_id=max_id
                    ))
                    await app(functions.stories.SendReactionRequest(
                        peer=username,
                        story_id=max_id,
                        reaction=types.ReactionEmoji(
                            emoticon='❤️'
                        ),
                        add_to_recent=True
                    ))
                    logger.log_info(f"Reaction has been given to @{username}")
            return stories_watched
        
    async def getAllPeerMaxIDsRequest(self, usernames):
        max_ids = []
        chunk_size = 60
        iter = 0
        while(iter + chunk_size < len(usernames)):
            chunk = usernames[iter:iter+chunk_size]

            max_ids_chunk = await self.app(functions.stories.GetPeerMaxIDsRequest(
                id=chunk
            ))
            max_ids.extend(max_ids_chunk)
            iter += chunk_size
            await asyncio.sleep(1)

        chunk = usernames[iter:iter+chunk_size]
        max_ids_chunk = await self.app(functions.stories.GetPeerMaxIDsRequest(
            id=chunk
        ))
        max_ids.extend(max_ids_chunk)
            
        return max_ids
            
        

    async def isUserAuthorized(self):
        await self.app.connect()
        result = await self.app.is_user_authorized()
        await self.app.disconnect()
        
        logger.log_info(
            f"Session {self.session_name} has been authorized successfully"
        ) if result else logger.log_warning(
            f"Session {self.session_name} has not been authorized successfully, it is either banned or not initialized"
        )
        return result 
    
    async def numberOfActiveStories(self, usernames):
        async with self.app as app:
            active_story_count = 0
            chunk_size = 60
            iter = 0
            while(iter + chunk_size < len(usernames)):
                chunk = usernames[iter:iter+chunk_size]

                max_ids = await app(functions.stories.GetPeerMaxIDsRequest(
                    id=chunk
                ))
                
                iter += chunk_size
                active_story_count += sum(1 for number in max_ids if number != 0)
                await asyncio.sleep(1)

            chunk = usernames[iter:]
            max_ids = await app(functions.stories.GetPeerMaxIDsRequest(
                id=chunk
            ))
            active_story_count += sum(1 for number in max_ids if number != 0)

        return active_story_count

async def main():
    x = UserAgentCore("test")
    result = await x.numberOfActiveStories(
        usernames=["Sergey_Pushkarev"]
    )
    print(result)


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())

