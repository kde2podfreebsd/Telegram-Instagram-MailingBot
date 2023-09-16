# from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from App.Database.Models import Base

# from sqlalchemy import create_engine
# from sqlalchemy import DateTime
# from sqlalchemy import ForeignKey
# from sqlalchemy import Text
# from sqlalchemy.dialects.postgresql import JSON
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from sqlalchemy.types import ARRAY


class TargetChannel(Base):
    __tablename__ = "target_channels"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    shortName = Column(String)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    username = Column
