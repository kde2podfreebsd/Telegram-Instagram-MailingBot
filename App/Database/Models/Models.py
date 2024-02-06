from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY

from App.Database.Models import Base


class AccountTg(Base):
    __tablename__ = "accounts_tg"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_file_path = Column(String, nullable=False)
    target_chat = Column(String, nullable=True, default="Не указан")
    message = Column(String, nullable=True, default="Не указано")
    prompt = Column(String, nullable=True, default="Не указан")
    advertising_channels = Column(MutableList.as_mutable(ARRAY(String)), nullable=True)
    status = Column(Boolean, nullable=False, default=False)

class AccountStories(Base):
    __tablename__ = "accounts_stories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_file_path = Column(String, nullable=False)
    target_channels = Column(MutableList.as_mutable(ARRAY(String)), nullable=True)
    aioscheduler_status = Column(Boolean, nullable=False, default=False)
    delay = Column(Integer, nullable=False, default=15)
 
    premium_chat_member = relationship("PremiumChatMember", back_populates="account_stories")

class PremiumChatMember(Base):
    __tablename__ = "premium_chat_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    account_stories_id = Column(Integer, ForeignKey('accounts_stories.id'))
    target_channel = Column(String, nullable=False)

    account_stories = relationship("AccountStories", back_populates="premium_chat_member")

class AccountInst(Base):
    __tablename__ = "accounts_inst"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_file_path = Column(String, nullable=False)
    target_channels = Column(MutableList.as_mutable(ARRAY(String)), nullable=True)
    message = Column(String, nullable=True, default="Не указано")
    status = Column(Boolean, nullable=False, default=False)
    
    followers = relationship("Follower", back_populates="account_inst")

class Follower(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    account_inst_id = Column(Integer, ForeignKey('accounts_inst.id'))
    target_channel = Column(String, nullable=False)

    account_inst = relationship("AccountInst", back_populates="followers")

