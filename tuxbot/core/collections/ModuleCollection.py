"""
Tuxbot collections module: ModuleCollection

Contains all module collections
"""
import importlib.util
from typing import TYPE_CHECKING, Type

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
            module_path = self.config["paths"]["python_cogs"] + f".{module_name}"

            module: Type[commands.Cog] = getattr(
                importlib.import_module(module_path, package='tuxbot'),
                module_name
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
            return logger.debug("[ModuleCollection] Skipping unknown module")

        module = _module(bot=self.bot)

        module.name = (
            module.name if hasattr(module, "name") else module.__cog_name__
        )
        active_module = self.bot.cogs.get(module.name)

        if active_module:
            logger.debug(f"[ModuleCollection] Unloading module {module.name}")
            self.bot.remove_cog(module.name)

        logger.debug(f"[ModuleCollection] Registering module {module.name}")

        self.bot.add_cog(module)

        logger.debug(
            f"[ModuleCollection] Added {len(tuple(module.walk_commands()))} "
            f"commands"
        )

        if hasattr(module, "models") and (models := module.models):
            self.register_models(models)

    # =========================================================================

    def register_models(self, models):
        """Register module models

        Parameters
        ----------
        models
            Module models to register
        """

        for model in models:
            logger.debug(f"[ModuleCollection] Registering model: {model.name}")
            self.bot.db.register_model()
