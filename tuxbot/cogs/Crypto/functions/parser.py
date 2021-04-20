import re
from typing import Optional


def data_parser(data: Optional[str]) -> dict:
    output = {
        "message": "",
        "compressed": False,
        "graphical": False,
        "chars": tuple,
    }

    if not data:
        return output

    if "--compressed" in data:
        output["compressed"] = True
        data = "".join(data.rsplit("--compressed", 1))

    if "--graphical" in data:
        output["graphical"] = True
        data = "".join(data.rsplit("--graphical", 1))

        if "compressed" in output.keys():
            del output["compressed"]

    if "--chars" in data:
        regex = r"--chars=(\S\S)"

        if match := re.search(regex, data):
            output["chars"] = tuple(match.group()[-2:])
            data = "".join(data.rsplit(match.group(), 1))

    output["message"] = data.strip()

    return output
