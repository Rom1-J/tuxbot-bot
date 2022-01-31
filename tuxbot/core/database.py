"""
Tuxbot core module: database

Manage database instance
"""
import glob
import importlib
from typing import Dict, Any, List, Tuple, TypeVar

from tortoise import Tortoise, ModelMeta

from tuxbot.core.config import config
from tuxbot.core.logger import logger

from tuxbot.core.models.Guild import GuildModel
from tuxbot.core.models.Tuxbot import TuxbotModel

# Note: adding models manually is not useful for the bot,
# it is only useful for the type hinting
M = TypeVar("M", TuxbotModel, GuildModel)


class Models:
    """Tuxbot models"""

    def __init__(self):
        self.__models: Dict[str, Tuple[str, M]] = {}

    def __setitem__(self, key: str, value: Tuple[str, M]):
        if self.check(value):
            logger.info("[Models] Adding model '%s'.", key)
            self.__models[key] = value

    def __getitem__(self, key: str) -> M:
        if model := self.__models.get(key):
            return model[1]

        raise KeyError

    # =========================================================================

    @staticmethod
    def check(value: Any):
        """Check for given value"""
        if (
            isinstance(value, tuple)
            and len(value) == 2
            and isinstance(value[0], str)
            and type(value[1])  # pylint: disable=unidiomatic-typecheck
            == ModelMeta
        ):
            return True

        logger.error(
            "[Models] Improper model value given (passed: %s).", value[1]
        )
        return False

    # =========================================================================

    def to_list(self) -> List[M]:
        """Return list of loaded models"""

        return [m[1] for m in self.__models.values()]

    def to_str_list(self) -> List[str]:
        """Return paths of loaded models"""

        return [m[0] for m in self.__models.values()]


class Database:
    """Tuxbot database"""

    models = Models()

    def __init__(self, c: Dict[str, Any]):
        self.config = c

    async def init(self):
        """Init database"""
        self.fetch_models()

        await Tortoise.init(
            config={
                "connections": {
                    "default": self.config["postgres"].get("dsn"),
                },
                "apps": {
                    "models": {
                        "models": self.models.to_str_list(),
                        "default_connection": "default",
                    }
                },
                "use_tz": False,
                "timezone": "UTC",
            },
        )
        await Tortoise.generate_schemas()

    def fetch_models(self):
        """fetch all models"""
        core_models = self.config["paths"].get("base") / "core" / "models"
        cwd = self.config["paths"].get("cwd")

        for module_path in glob.glob(f"{core_models}/*.py"):
            module_path = (
                module_path.replace(str(cwd), "")[:-3]
                .lstrip("/")
                .replace("/", ".")
            )
            module_name = module_path.split(".")[-1]

            module = importlib.import_module(module_path)

            if model := getattr(module, module_name + "Model", None):
                self.models[module_name] = (module_path, model)


db = Database(config)
