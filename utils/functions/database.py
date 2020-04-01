from .config import Config

import sqlalchemy
import databases


class Database:
    def __init__(self, config: Config):
        conf_postgresql = config["postgresql"]
        postgresql = 'postgresql://{}:{}@{}/{}'.format(
            conf_postgresql.get("Username"), conf_postgresql.get("Password"),
            conf_postgresql.get("Host"), conf_postgresql.get("DBName"))

        self.database = databases.Database(postgresql)
        self.metadata = sqlalchemy.MetaData()
        self.engine = sqlalchemy.create_engine(str(self.database.url))
