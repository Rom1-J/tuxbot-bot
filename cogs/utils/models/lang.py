from . import Base
from sqlalchemy import Column, String


class LangModel(Base):
    __tablename__ = 'langs'

    key = Column(String, primary_key=True)
    value = Column(String)

    def __repr__(self):
        return "<LangModel(key='%s', locale='%s')>" % (self.key, self.value)
