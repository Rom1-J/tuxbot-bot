from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, BigInteger, JSON, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Poll(Base):
    __tablename__ = 'polls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger)
    message_id = Column(BigInteger)

    content = Column(JSON)

    choice = relationship("Responses")


class Responses(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Text)

    poll_id = Column(Integer, ForeignKey('polls.id'))
    choice = Column(Integer)
