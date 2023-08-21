"""Emotes used by TuxBot."""


class Emotes:
    """Enum of all different emotes used."""

    ALPHABET: tuple[str, ...] = tuple(chr(0x1F1E6 + i) for i in range(26))

    # https://cdn.discordapp.com/emojis/596577462335307777.webp
    PYTHON: str = "<:python:596577462335307777>"

    # https://cdn.discordapp.com/emojis/851473526992797756.webp
    WOLFRAMALPHA: str = "<:wolframalpha:851473526992797756>"
