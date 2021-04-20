import sys
from tuxbot import ExitCodes
from tuxbot.core.utils.console import console


def main() -> None:
    try:
        from .__run__ import run  # pylint: disable=import-outside-toplevel

        run()
    except SystemExit as exc:
        if exc.code == ExitCodes.RESTART:
            sys.exit(exc.code)
        else:
            raise exc
    except Exception:
        console.print_exception(
            show_locals=True, word_wrap=True, extra_lines=5
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        console.print_exception(
            show_locals=True, word_wrap=True, extra_lines=5
        )
