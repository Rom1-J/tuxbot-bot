import re
import sys
from pathlib import Path

from rich.prompt import Prompt, Confirm

from tuxbot.core.utils.console import console

INIT_TEMPLATE = """from collections import namedtuple

from tuxbot.core.bot import Tux
from .{lower_name} import {name}
from .config import {name}Config, HAS_MODELS

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=1, minor=0, micro=0, release_level="alpha")

__version__ = "v{{}}.{{}}.{{}}-{{}}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\\n", "")


def setup(bot: Tux):
    bot.add_cog({name}(bot))

"""


CONFIG_TEMPLATE = """from typing import Dict

from structured_config import Structure

HAS_MODELS = {has_models}


class {name}Config(Structure):
    pass


extra: Dict[str, Dict] = {{}}

"""


MODULE_TEMPLATE = """import logging
from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.{name}")
_ = Translator("{name}", __file__)


class {name}(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @command_extra(name="to_replace", deletable=True)
    async def _to_replace(self, ctx: ContextPlus):
        ...

    # =========================================================================

"""

MESSAGES_TEMPLATE = """# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the Tuxbot-bot package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: Tuxbot-bot\\n"
"Report-Msgid-Bugs-To: rick@gnous.eu\\n"
"POT-Creation-Date: 2021-05-17 00:04+0200\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: 8bit\\n"

"""


def get_name() -> str:
    name = ""
    while not name:
        name = Prompt.ask(
            "What name do you want to give this instance?\n"
            "[i](valid characters: A-Z, a-z, 0-9, _, -)[/i]\n",
            console=console,
        )
        if re.fullmatch(r"[a-zA-Z0-9_\-]*", name) is None:
            console.print()
            console.print("[prompt.invalid]ERROR: Invalid characters provided")
            name = ""

    return name.replace("-", " ").capitalize().replace(" ", "")


def get_has_models() -> bool:
    return Confirm.ask(
        "Does this cog use models?", default=False, console=console
    )


def write(path: Path, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def generate(name: str, has_models: bool) -> None:
    init = INIT_TEMPLATE.format(
        lower_name=name.lower(), name=name, has_models=has_models
    )
    config = CONFIG_TEMPLATE.format(name=name, has_models=has_models)
    module = MODULE_TEMPLATE.format(name=name, has_models=has_models)

    # =========================================================================

    path = Path("tuxbot") / "cogs" / name
    if path.exists():
        console.log("This cog already exists")
        sys.exit(1)

    path.mkdir()

    write(path / "__init__.py", init)
    write(path / "config.py", config)
    write(path / f"{name.lower()}.py", module)

    # =========================================================================

    functions_path = path / "functions"
    functions_path.mkdir()

    write(functions_path / "__init__.py", "")

    # =========================================================================

    models_path = path / "models"
    models_path.mkdir()

    write(models_path / "__init__.py", "")

    # =========================================================================

    locales_path = path / "locales"
    locales_path.mkdir()

    write(locales_path / "messages.pot", MESSAGES_TEMPLATE)


def main():
    name = get_name()
    has_models = get_has_models()

    generate(name, has_models)

    console.log("Done!")


if __name__ == "__main__":
    main()
