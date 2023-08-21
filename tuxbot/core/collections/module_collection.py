"""
Tuxbot collections module: ModuleCollection.

Contains all module collections
"""
import importlib
import inspect
import typing
from pathlib import Path

from discord.ext import commands

from tuxbot.core.config import config


if typing.TYPE_CHECKING:
    from tuxbot.abc.module_abc import ModuleABC
    from tuxbot.core.tuxbot import Tuxbot


class ModuleCollection:
    """Tuxbot modules collection."""

    _modules: dict[str, list[commands.Cog]]

    def __init__(self: typing.Self, bot: "Tuxbot") -> None:
        self.bot = bot

        self._modules = {}

    # =========================================================================

    def add_module(self: typing.Self, name: str, module: commands.Cog) -> None:
        """Preload modules."""
        module.__cog_name__ = f"{name}_{module.__cog_name__}"

        if name not in self._modules:
            self._modules[name] = [module]
        else:
            self._modules[name].append(module)

    # =========================================================================

    async def load_modules(self: typing.Self) -> None:
        """Load all modules from config."""
        if not (modules := config.INSTALLED_COGS):
            return

        for module_path in modules:
            module_name = module_path.split(".")[-1].title()

            module: type[commands.Cog | "ModuleABC"] = getattr(
                importlib.import_module(module_path),
                module_name,
            )

            await self.register(module)

    # =========================================================================

    async def register(self: typing.Self, _module: type[commands.Cog]) -> None:
        """
        Register module.

        Parameters
        ----------
        _module: type[commands.Cog]
            Module class to register
        """
        if not isinstance(_module, commands.CogMeta):
            self.bot.logger.exception(
                "[ModuleCollection] Skipping unknown module"
            )
            return

        module = _module(bot=self.bot)
        module_path = Path(inspect.getfile(_module))

        active_module = self.bot.cogs.get(module.qualified_name)

        if active_module:
            self.bot.logger.info(
                "[ModuleCollection] Unloading module '%s'",
                module.qualified_name,
            )
            await self.bot.remove_cog(module.qualified_name)

        self.bot.logger.info(
            "[ModuleCollection] Registering module '%s'", module.qualified_name
        )

        await self.bot.add_cog(module)

        if sub_modules := self._modules.get(module.qualified_name):
            for sub_module in sub_modules:
                sub_module.cog_check = module.cog_check
                await self.bot.add_cog(sub_module)

        self.register_models(module_path.glob("**/models/*.py"))

    # =========================================================================

    def register_models(
        self: typing.Self, models: typing.Iterator[Path]
    ) -> None:
        """
        Register module models.

        Parameters
        ----------
        models: list[str]
            Module models to register
        """
        for model in models:
            self.bot.db.register_model(
                Path(str(model).split("site-packages/")[-1])
            )
