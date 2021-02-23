import re


def data_parser(data: str) -> dict:
    output = {
        "message": None,
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
        match = re.search(regex, data)

        output["chars"] = tuple(match.group()[-2:])
        data = "".join(data.rsplit(match.group(), 1))

    output["message"] = data.strip()

    return output
