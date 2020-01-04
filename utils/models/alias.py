from sqlalchemy import Column, String, BigInteger, Integer

from . import Base


class AliasesModel(Base):
    __tablename__ = 'aliases'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    alias = Column(String)
    command = Column(String)
    guild = Column(String)

    def __repr__(self):
        return "<AliasesModel(" \
               "id='%s', " \
               "user_id='%s', " \
               "alias='%s', " \
               "command='%s', " \
               "guild='%s', " \
               ")>" % (
                   self.id,
                   self.user_id,
                   self.alias,
                   self.command,
                   self.guild
               )
