from . import Base
from sqlalchemy import Column, Integer, BigInteger, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class PollModel(Base):
    __tablename__ = 'polls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger)
    message_id = Column(BigInteger)

    content = Column(JSON)
    is_anonymous = Column(Boolean)

    available_choices = Column(Integer)
    choice = relationship("ResponsesModel")


class ResponsesModel(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(BigInteger)

    poll_id = Column(Integer, ForeignKey('polls.id'))
    choice = Column(Integer)
