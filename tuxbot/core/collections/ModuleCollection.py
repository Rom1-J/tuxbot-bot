"""
Tuxbot collections module: ModuleCollection

Contains all module collections
"""
import glob
import importlib.util
import inspect
import os
from typing import TYPE_CHECKING, List, Type

from discord.ext import commands

from tuxbot.core.logger import logger

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class ModuleCollection:
    """Tuxbot modules collection"""

    def __init__(self, config, bot: "Tuxbot"):
        self.config = config
        self.bot = bot

    # =========================================================================

    def load_modules(self):
        """Load all modules from config"""
        if not (modules := self.config["modules"]):
            return

        for module_name in modules:
            module_path = (
                self.config["paths"]["python_cogs"] + f".{module_name}"
            )

            module: Type[commands.Cog] = getattr(
                importlib.import_module(module_path, package="tuxbot"),
                module_name,
            )

            self.register(module)

    # =========================================================================

    def register(self, _module: Type[commands.Cog]):
        """Register module

        Parameters
        ----------
        _module: Type[commands.Cog]
            Module class to register
        """
        if not isinstance(_module, commands.CogMeta):
            logger.error("[ModuleCollection] Skipping unknown module")
            return

        module = _module(bot=self.bot)
        module_path = os.path.dirname(inspect.getfile(_module))

        module.name = (
            module.name if hasattr(module, "name") else module.__cog_name__
        )
        active_module = self.bot.cogs.get(module.name)

        if active_module:
            logger.info(
                "[ModuleCollection] Unloading module '%s'", module.name
            )
            self.bot.remove_cog(module.name)

        logger.info("[ModuleCollection] Registering module '%s'", module.name)

        self.bot.add_cog(module)
        self.register_models(
            glob.glob(f"{module_path}/**/models/*.py", recursive=True)
        )

    # =========================================================================

    def register_models(self, models: List[str]):
        """Register module models

        Parameters
        ----------
        models:List[str]
            Module models to register
        """

        for model in models:
            self.bot.db.register_model(model)  # type: ignore
