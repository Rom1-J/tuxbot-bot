"""Global embed page."""
import typing

import discord

from .embed import Embed


class GlobalEmbed(Embed):
    """Global embed page."""

    def rebuild(self: typing.Self) -> discord.Embed:
        """(Re)build embed."""
        rir = str(self.controller.get_data("ipwhois", "asn_registry"))
        cidr = str(self.controller.get_data("ipwhois", "asn_cidr"))

        e = discord.Embed(
            color=0x1E448A,
            title=(
                f"Information for ``{self.controller.get_data('domain')} "
                f"({self.controller.get_data('ip')})``"
            ),
        )

        e.description = (
            f"```"
            f"{self.controller.get_data('ipinfo', 'city')} - "
            f"{self.controller.get_data('ipinfo', 'region')} "
            f"({self.controller.get_data('ipinfo', 'country_name')})"
            f"```"
        )

        e.add_field(
            name="Belongs to",
            value=f"```{self.controller.get_data('ipinfo', 'org')}```",
            inline=True,
        )

        if isinstance(
            nets := self.controller.get_data("ipwhois", "nets"), list
        ):
            if created := nets[0].get("created", None):
                created = created.replace("T", " ").split("Z")[0]

            if updated := nets[0].get("updated", None):
                updated = updated.replace("T", " ").split("Z")[0]

            e.add_field(
                name="Description",
                value="```{}```".format(nets[0].get("description", "N/A")),
                inline=False,
            )

            e.add_field(
                name="Name",
                value=f"``` {nets[0].get('name', 'N/A')} ```",
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

            if emails := nets[0].get("emails", False):
                e.add_field(
                    name="Emails",
                    value=f"```{' | '.join(emails)}```",
                    inline=False,
                )

        e.add_field(
            name="Route",
            value=f"[{cidr}](https://bgp.he.net/net/{cidr}/)",
            inline=True,
        )
        e.add_field(
            name="RIR",
            value=(
                f"[{rir.upper()}]"
                f"(https://www.iana.org/numbers/allocations/{rir}/asn/)"
            ),
            inline=True,
        )

        e.set_thumbnail(
            url=(
                "https://flagcdn.com/144x108/"
                f"{str(self.controller.get_data('ipinfo', 'country')).lower()}"
                ".png"
            )
        )

        e.set_footer(
            text=f"Hostname: {self.controller.get_data('hostname')}",
        )

        return e
