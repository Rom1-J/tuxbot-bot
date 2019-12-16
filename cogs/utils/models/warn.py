import datetime

from . import Base
from sqlalchemy import Column, Integer, String, BIGINT, TIMESTAMP


class Warn(Base):
    __tablename__ = 'warns'

    id = Column(Integer, primary_key=True)
    server_id = Column(BIGINT)
    user_id = Column(BIGINT)
    reason = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())

    def __repr__(self):
        return "<Warn(server_id='%s', user_id='%s', reason='%s', " \
               "created_at='%s')>" \
               % (self.server_id, self.user_id, self.reason, self.created_at)
