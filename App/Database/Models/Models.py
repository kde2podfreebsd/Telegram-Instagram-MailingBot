from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY

from App.Database.Models import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_file_path = Column(String, nullable=False)
    target_chat = Column(String, nullable=True, default="Не указан")
    message = Column(String, nullable=True, default="Не указано")
    prompt = Column(String, nullable=True, default="Не указан")
    advertising_channels = Column(MutableList.as_mutable(ARRAY(String)), nullable=True)
    status = Column(Boolean, nullable=False, default=False)

    chat_members = relationship("ChatMember", back_populates="account")


class ChatMember(Base):
    __tablename__ = "telegram_chat_members"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    is_premium = Column(Boolean, nullable=False)

    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="chat_members")
