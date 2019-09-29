from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
Base = declarative_base()


class Lang(Base):
    __tablename__ = 'lang'

    key = Column(String, primary_key=True)
    value = Column(String)

    def __repr__(self):
        return "<Lang(key='%s', locale='%s')>" % (self.key, self.value)
