from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session


class Database:
    def __init__(self, config):
        self.engine = create_engine(config.postgresql, echo=True)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session: session = Session()
