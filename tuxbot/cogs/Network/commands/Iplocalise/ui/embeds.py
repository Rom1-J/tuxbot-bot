import json
from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from .view import ViewController


class Embeds:
    def __init__(self, controller: "ViewController"):
        self.controller = controller

        self.ctx = self.controller.ctx
        self.data = self.controller.data

    # =========================================================================
    # =========================================================================

    async def global_embed(self) -> discord.Embed:
        rir = self.data["ipwhois"].get("asn_registry", "N/A")
        cidr = self.data["ipwhois"].get("asn_cidr", "N/A")

        e = discord.Embed(
            color=0x1E448A,
            title=f"Information for ``{self.data['domain']} "
            f"({self.data['ip']})``",
        )

        e.description = (
            f"```"
            f'{self.data["ipgeo"].get("organization", "")}\n\n'
            f'{self.data["ipinfo"].get("city", "")} - '
            f'{self.data["ipinfo"].get("region", "")} '
            f'({self.data["ipinfo"].get("country_name", "")})'
            f"```"
        )

        e.add_field(
            name="Belongs to",
            value=f'```{self.data["ipinfo"].get("org", "N/A")}```',
            inline=True,
        )

        if "nets" in self.data["ipwhois"]:
            if created := self.data["ipwhois"]["nets"][0].get("created", None):
                created = created.replace("T", " ").split("Z")[0]

            if updated := self.data["ipwhois"]["nets"][0].get("updated", None):
                updated = updated.replace("T", " ").split("Z")[0]

            e.add_field(
                name="Description",
                value=f'```{self.data["ipwhois"]["nets"][0].get("description", "N/A")}```',
                inline=False,
            )

            e.add_field(
                name="Name",
                value=f"```"
                f'{self.data["ipwhois"]["nets"][0].get("name", "N/A")}'
                f"```",
                inline=True,
            )
            e.add_field(
                name="Created",
                value=f"```{created}```",
                inline=True,
            )
            e.add_field(
                name="Updated",
                value=f"```{updated}```",
                inline=True,
            )

            if emails := self.data["ipwhois"]["nets"][0].get("emails", False):
                e.add_field(
                    name="Emails",
                    value=f'```{" | ".join(emails)}```',
                    inline=False,
                )

        e.add_field(
            name="Route",
            value=f"[{cidr}](https://bgp.he.net/net/{cidr}/)",
            inline=True,
        )
        e.add_field(
            name="RIR",
            value=f"[{rir.upper()}](https://www.iana.org/numbers/allocations/{rir}/asn/)",
            inline=True,
        )

        e.set_thumbnail(
            url=f"https://flagcdn.com/144x108/"
            f'{self.data["ipinfo"].get("country", "").lower()}'
            f".png"
        )

        e.set_footer(
            text=f"Hostname: {self.data['ipinfo'].get('hostname', 'N/A')}",
        )

        return e

    # =========================================================================

    async def geo_embed(self) -> discord.Embed:
        e = discord.Embed(
            color=0xB2157E,
            title=f"Location for ``{self.data['domain']} "
            f"({self.data['ip']})``",
        )

        if self.data["opencage"] and (
            results := self.data["opencage"]["results"]
        ):
            result = results[0]
            annotations = result["annotations"]
            timezone = annotations["timezone"]

            latlon = " ".join(annotations["DMS"].values())
            map_url = annotations["OSM"].get("url", "")

            currency = annotations["currency"]

            e.description = f"[{latlon}]({map_url})"

            e.add_field(
                name="Currency",
                value=f"```"
                f'{currency["name"]} '
                f'({currency["symbol"]} | {currency["iso_code"]})'
                f"```",
                inline=True,
            )
            e.add_field(
                name="Timezone",
                value=f"```"
                f'{timezone["name"]} '
                f'({timezone["offset_string"]})'
                f"```",
                inline=True,
            )
            e.add_field(
                name="Phone",
                value=f"```" f'+{annotations["callingcode"]} ' f"```",
                inline=True,
            )

        if map_url := self.data["map"].get("url", ""):
            e.set_image(url=map_url)

        return e

    # =========================================================================

    async def raw_embed(self) -> discord.Embed:
        e = discord.Embed(
            title=f"Raw data for ``{self.data['domain']} "
            f"({self.data['ip']})``",
        )

        fail, output = await self.ctx.bot.utils.shorten(
            json.dumps(self.data, indent=2), 4000
        )

        e.description = (
            f"```json\n{output['text']}```" if fail else output["link"]
        )

        return e
