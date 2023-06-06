"""Import other functions"""
from sqlalchemy import Column, Integer, String
from init import Base, engine


class User(Base):
    """registers users to keep track of e.g. e-exp"""
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    e_exp = Column(Integer)

class Channel(Base):
    """registers channel features"""
    __tablename__ = "Channel"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(Integer)
    channel_id = Column(Integer)
    channel_type = Column(String)
    # Channel Types:
    # None, Singing, Moderation

Base.metadata.create_all(engine)
