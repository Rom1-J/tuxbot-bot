import codecs
import itertools
import sys


def bordered(*columns: dict) -> str:
    """
    credits to https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/core/utils/chat_formatting.py

    Get two blocks of text in a borders.

    Note
    ----
    This will only work with a monospaced font.

    Parameters
    ----------
    *columns : `sequence` of `str`
        The columns of text, each being a list of lines in that column.

    Returns
    -------
    str
        The bordered text.

    """
    encoder = codecs.getencoder(sys.stdout.encoding)
    try:
        encoder("┌┐└┘─│")  # border symbols
    except UnicodeEncodeError:
        ascii_border = True
    else:
        ascii_border = False

    borders = {
        "TL": "+" if ascii_border else "┌",  # Top-left
        "TR": "+" if ascii_border else "┐",  # Top-right
        "BL": "+" if ascii_border else "└",  # Bottom-left
        "BR": "+" if ascii_border else "┘",  # Bottom-right
        "HZ": "-" if ascii_border else "─",  # Horizontal
        "VT": "|" if ascii_border else "│",  # Vertical
    }

    sep = " " * 4  # Separator between boxes
    widths = tuple(
        max(
            len(row) for row in column.get('rows')
        ) + 9
        for column in columns
    )  # width of each col
    cols_done = [False] * len(columns)  # whether or not each column is done
    lines = [""]

    for i, column in enumerate(columns):
        lines[0] += "{TL}" + "{HZ}" + column.get('title') \
                    + "{HZ}" * (widths[i] - len(column.get('title')) - 1) \
                    + "{TR}" + sep

    for line in itertools.zip_longest(
            *[column.get('rows') for column in columns]
    ):
        row = []
        for colidx, column in enumerate(line):
            width = widths[colidx]
            done = cols_done[colidx]
            if column is None:
                if not done:
                    # bottom border of column
                    column = "{HZ}" * width
                    row.append("{BL}" + column + "{BR}")
                    cols_done[colidx] = True  # mark column as done
                else:
                    # leave empty
                    row.append(" " * (width + 2))
            else:
                column += " " * (width - len(column))  # append padded spaces
                row.append("{VT}" + column + "{VT}")

        lines.append(sep.join(row))

    final_row = []
    for width, done in zip(widths, cols_done):
        if not done:
            final_row.append("{BL}" + "{HZ}" * width + "{BR}")
        else:
            final_row.append(" " * (width + 2))
    lines.append(sep.join(final_row))

    return "\n".join(lines).format(**borders)
