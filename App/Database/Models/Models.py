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

class TargetChannel(Base):
    __tablename__ = "target_channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    premium_members = Column(MutableList.as_mutable(ARRAY(String)), nullable=True) 

class AccountInst(Base):
    __tablename__ = "accounts_inst"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_file_path = Column(String, nullable=False)
    target_channel = Column(String, nullable=True, default="Не указан")
    message = Column(String, nullable=True, default="Не указано")
    status = Column(Boolean, nullable=False, default=False)
    
    followers = relationship("Follower", back_populates="account_inst")

class Follower(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    account_inst_id = Column(Integer, ForeignKey('accounts_inst.id'))

    account_inst = relationship("AccountInst", back_populates="followers")

