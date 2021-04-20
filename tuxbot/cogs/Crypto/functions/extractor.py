from typing import Optional, NoReturn, Union

from discord import Attachment
from tuxbot.cogs.Crypto.functions.parser import data_parser


async def extract(
    attachments: list[Optional[Attachment]], data: Optional[str], max_size: int
) -> dict:
    if not data and len(attachments) == 0:
        raise ValueError

    kwargs = data_parser(data)

    if attachments and attachments[0]:
        file: Attachment = attachments[0]
        if file.size > max_size:
            raise ValueError

        kwargs["message"] = await file.read()

    params = {
        "compressed": "compressed" in kwargs.keys(),
        "graphical": "graphical" in kwargs.keys(),
        "chars": kwargs["chars"] if "chars" in kwargs.keys() else (".", ","),
    }

    return {"message": kwargs["message"], "params": params}
