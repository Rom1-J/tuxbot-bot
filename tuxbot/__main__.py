import sys
from tuxbot import ExitCodes


def main() -> None:
    try:
        from .__run__ import run  # pylint: disable=import-outside-toplevel

        run()
    except SystemExit as exc:
        if exc.code == ExitCodes.RESTART:
            sys.exit(exc.code)
        else:
            raise exc


if __name__ == "__main__":
    main()
