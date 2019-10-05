from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, BigInteger, JSON

Base = declarative_base()


class Poll(Base):
    __tablename__ = 'polls'

    id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger)
    poll = Column(JSON)
    is_anonymous = Column(Boolean)
    responses = Column(JSON, nullable=True)

    def __repr__(self):
        return "<Poll(id='%s', message_id='%s', poll='%s', " \
               "is_anonymous='%s', responses='%s')>" % \
               (self.id, self.message_id, self.poll,
                self.is_anonymous, self.responses)
