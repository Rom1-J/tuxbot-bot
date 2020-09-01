from typing import NoReturn

from rich.console import Console
from rich.traceback import install
from tuxbot import ExitCodes

console = Console()
install(console=console)


def main() -> NoReturn:
    try:
        from .__run__ import run

        run()
    except SystemExit as exc:
        if exc.code == ExitCodes.RESTART:
            from .__run__ import run  # reimport to load changes
            run()
        else:
            raise exc
    except Exception:
        console.print_exception()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        console.print_exception()
