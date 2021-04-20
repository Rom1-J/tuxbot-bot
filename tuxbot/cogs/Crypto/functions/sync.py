# from io import BytesIO
# from typing import Union
#
# import discord
# from ralgo.ralgo import Ralgo
# from tuxbot.cogs.Crypto.functions.file import find_ext
#
#
# def encode(params: dict) -> Union[str, discord.File]:
#     statement = Ralgo(params["message"])
#     params = params["params"]
#     encoded = statement.encode(chars=params["chars"])
#
#     if params["compressed"]:
#         return str(encoded.compress())
#     if params["graphical"]:
#         output = encoded.graphical().encode()
#         return discord.File(BytesIO(output.to_bytes()), "output.png")
#
#     return str(encoded)
#
#
# def decode(params: dict) -> Union[str, discord.File]:
#     statement = Ralgo(params["message"])
#     params = params["params"]
#
#     if params["graphical"]:
#         output = Ralgo(statement.graphical().decode()).decode()
#     elif params["compressed"]:
#         output = Ralgo(statement.decompress()).decode()
#     else:
#         output = statement.decode(chars=params["chars"])
#
#     if isinstance(output, bytes):
#         return discord.File(BytesIO(output), f"output.{find_ext(output)}")
#
#     output = discord.utils.escape_markdown(str(output))
#     output = discord.utils.escape_mentions(output)
#
#     return output if len(output) > 0 else "no content..."
