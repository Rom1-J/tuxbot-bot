from .config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session


class Database:
    def __init__(self, config: Config):
        conf_postgresql = config["postgresql"]
        postgresql = 'postgresql://{}:{}@{}/{}'.format(
            conf_postgresql.get("Username"), conf_postgresql.get("Password"),
            conf_postgresql.get("Host"), conf_postgresql.get("DBName"))
        self.engine = create_engine(postgresql, echo=False)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session: session = Session()
