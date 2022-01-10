"""
Tuxbot collections module: ModuleCollection

Contains all module collections
"""
import importlib.util
from collections.abc import MutableMapping
from typing import TYPE_CHECKING, Iterator, Dict, Type

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.logger import logger

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class ModuleCollection(MutableMapping):
    """Tuxbot modules collection"""

    _modules: Dict[str, ModuleABC] = {}

    def __setitem__(self, key: str, value: ModuleABC) -> None:
        self._modules[key] = value

    def __delitem__(self, key: str) -> None:
        del self._modules[key]

    def __getitem__(self, key: str) -> ModuleABC:
        return self._modules[key]

    def __len__(self) -> int:
        return len(self._modules)

    def __iter__(self) -> Iterator[str]:
        return self._modules.__iter__()

    def __init__(self, config, tuxbot: "Tuxbot"):
        self.config = config
        self.tuxbot = tuxbot

    # =========================================================================

    async def load_modules(self):
        """Load all modules from config"""
        for module_name in self.config["modules"]:
            module_path = self.config["paths"]["commands"] + f".{module_name}"

            module: Type[ModuleABC] = getattr(
                importlib.import_module(module_path, package='tuxbot'),
                f"{module_name}Module"
            )

            self.register(module)

    # =========================================================================

    def register(self, _module: Type[ModuleABC]):
        """Register module

        Parameters
        ----------
        _module:ModuleABC
            Module class to register
        """
        if not _module.__base__.__name__ == "ModuleABC":
            return logger.debug("[ModuleCollection] Skipping unknown module")

        module = _module(self.tuxbot)
        active_module = self._modules.get(module.name)

        if active_module:
            logger.debug(f"[ModuleCollection] Unloading module {module.name}")
            active_module.cog_unload()
            del self._modules[module.name]

        logger.debug(f"[ModuleCollection] Registering module {module.name}")

        self.tuxbot.add_cog(module)

        if models := module.models:
            self.register_models(models)

        self._modules[module.name] = module

        for event in self.tuxbot.dispatcher.events:
            if not hasattr(module, event):
                continue

            module.register_listener(event, getattr(module, event))

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
            self.tuxbot.db.register_model()
