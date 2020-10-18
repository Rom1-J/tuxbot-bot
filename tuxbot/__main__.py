from typing import NoReturn

from rich.console import Console
from rich.traceback import install
from tuxbot import ExitCodes

console = Console()
install(console=console)


def main() -> NoReturn:
    try:
        from .__run__ import run  # pylint: disable=import-outside-toplevel

        run()
    except SystemExit as exc:
        if exc.code == ExitCodes.RESTART:
            # reimport to load changes
            from .__run__ import run  # pylint: disable=import-outside-toplevel

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
