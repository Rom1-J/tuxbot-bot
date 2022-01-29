"""
tuxbot.cogs.Utils.commands.Info.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of utils functions
"""

import os
import pathlib
from typing import Any, Dict

import aiofiles


async def fetch_info(paths: dict) -> Dict[str, Any]:
    """Fetch set of information about tuxbot"""

    total_lines = 0

    total_python_class = 0
    total_python_functions = 0
    total_python_coroutines = 0
    total_python_comments = 0

    file_amount = 0
    python_file_amount = 0

    for path, _, files in os.walk(paths.get("base", "./")):
        for name in files:
            file_dir = str(pathlib.PurePath(path, name))
            if (
                name.split(".")[-1] not in ("py", "po", "json", "png")
            ) or "env" in file_dir:
                continue

            file_amount += 1

            if name.endswith(".py"):
                python_file_amount += 1

                async with aiofiles.open(
                    file_dir, "r", encoding="utf-8"
                ) as file:
                    async for line in file:
                        line = line.strip()
                        if line.startswith("class"):
                            total_python_class += 1
                        if line.startswith("def"):
                            total_python_functions += 1
                        if line.startswith("async def"):
                            total_python_coroutines += 1
                        if "#" in line:
                            total_python_comments += 1
                        total_lines += 1

    return {
        "total_lines": total_lines,
        "total_python_class": total_python_class,
        "total_python_functions": total_python_functions,
        "total_python_coroutines": total_python_coroutines,
        "total_python_comments": total_python_comments,
        "file_amount": file_amount,
        "python_file_amount": python_file_amount,
    }
