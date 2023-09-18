# from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import ARRAY

from App.Database.Models import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_file_path = Column(String, nullable=False)
    target_chat = Column(String, nullable=False)
    message = Column(String, nullable=True)
    advertising_channels = Column(MutableList.as_mutable(ARRAY(String)), nullable=True)
