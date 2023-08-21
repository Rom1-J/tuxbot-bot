"""Geo embed page."""

import typing

import discord

from .embed import Embed


class GeoEmbed(Embed):
    """Geo embed page."""

    def rebuild(self: typing.Self) -> discord.Embed:
        """(Re)build embed."""
        e = discord.Embed(
            color=0xB2157E,
            title=(
                f"Information for ``{self.controller.get_data('domain')} "
                f"({self.controller.get_data('ip')})``"
            ),
        )

        if (
            self.controller.get_data("opencage") != "Pending..."
            and (results := self.controller.get_data("opencage", "results"))
            and isinstance(results, list)
            and results
        ):
            result: dict[str, typing.Any] = results[0]
            annotations = result["annotations"]
            timezone = annotations["timezone"]

            latlon = " ".join(annotations["DMS"].values())
            map_url = annotations["OSM"].get("url", "")

            currency = annotations["currency"]

            e.description = f"[{latlon}]({map_url})"

            e.add_field(
                name="Currency",
                value=(
                    "```"
                    f"{currency['name']} "
                    f"({currency['symbol']} | {currency['iso_code']})"
                    "```"
                ),
                inline=True,
            )
            e.add_field(
                name="Timezone",
                value=(
                    "```"
                    f"{timezone['name']} "
                    f"({timezone['offset_string']})"
                    "```"
                ),
                inline=True,
            )
            e.add_field(
                name="Phone",
                value=f"``` +{annotations['callingcode']} ```",
                inline=True,
            )

        if self.controller.get_data("map") != "Pending..." and (
            map_url := self.controller.get_data("map", "url")
        ):
            e.set_image(url=map_url)

        return e
