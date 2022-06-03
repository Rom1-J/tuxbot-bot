"""
Tuxbot collections module: ModuleCollection

Contains all module collections
"""
import glob
import importlib.util
import inspect
import os
from typing import TYPE_CHECKING, Dict, List, Type, Union

from discord.ext import commands


if TYPE_CHECKING:
    from tuxbot.abc.ModuleABC import ModuleABC
    from tuxbot.core.Tuxbot import Tuxbot


class ModuleCollection:
    """Tuxbot modules collection"""

    _modules: Dict[str, List[commands.Cog]]

    def __init__(self, config, bot: "Tuxbot"):
        self.config = config
        self.bot = bot

        self._modules = {}

    # =========================================================================

    def add_module(self, name: str, module: commands.Cog):
        """Preload modules"""

        module.__cog_name__ = f"{name}_{module.__cog_name__}"

        if name not in self._modules:
            self._modules[name] = [module]
        else:
            self._modules[name].append(module)

    # =========================================================================

    async def load_modules(self):
        """Load all modules from config"""
        if not (modules := self.config["modules"]):
            return

        for module_name in modules:
            module_path = (
                self.config["paths"]["python_cogs"] + f".{module_name}"
            )

            module: Type[Union["ModuleABC", commands.Cog]] = getattr(
                importlib.import_module(module_path, package="tuxbot"),
                module_name,
            )

            await self.register(module)

    # =========================================================================

    async def register(self, _module: Type[commands.Cog]):
        """Register module

        Parameters
        ----------
        _module: Type[commands.Cog]
            Module class to register
        """
        if not isinstance(_module, commands.CogMeta):
            self.bot.logger.error("[ModuleCollection] Skipping unknown module")
            return

        module = _module(bot=self.bot)
        module_path = os.path.dirname(inspect.getfile(_module))

        module.name = (
            module.name if hasattr(module, "name") else module.__cog_name__
        )
        active_module = self.bot.cogs.get(module.name)

        if active_module:
            self.bot.logger.info(
                "[ModuleCollection] Unloading module '%s'", module.name
            )
            await self.bot.remove_cog(module.name)

        self.bot.logger.info(
            "[ModuleCollection] Registering module '%s'", module.name
        )

        await self.bot.add_cog(module)

        if sub_modules := self._modules.get(module.name):
            for sub_module in sub_modules:
                sub_module.cog_check = module.cog_check
                await self.bot.add_cog(sub_module)

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
            # type: ignore
            self.bot.db.register_model(model.split("site-packages/")[-1])
