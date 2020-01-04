from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from .lang import LangModel
from .warn import WarnModel
from .poll import PollModel, ResponsesModel
from .alias import AliasesModel
