from typing import Optional, List

from tuxbot.cogs.Mod.models import MuteRole
from tuxbot.cogs.Mod.models.rules import Rule
from tuxbot.core.config import set_for_key
from tuxbot.core.config import Config

from tuxbot.core.bot import Tux
from tuxbot.core.utils.functions.extra import ContextPlus


async def save_lang(bot: Tux, ctx: ContextPlus, lang: str) -> None:
    set_for_key(bot.config.Servers, ctx.guild.id, Config.Server, locale=lang)


async def get_server_rules(guild_id: int) -> List[Rule]:
    return await Rule.filter(server_id=guild_id).all().order_by("rule_id")


def get_most_recent_server_rules(rules: List[Rule]) -> Rule:
    return sorted(rules, key=lambda r: r.updated_at, reverse=True)[0]


def paginate_server_rules(rules: List[Rule]) -> List[str]:
    body = [""]

    for rule in rules:
        if len(body[-1] + format_rule(rule)) > 2000:
            body.append(format_rule(rule) + "\n")
        else:
            body[-1] += format_rule(rule) + "\n"

    return body


def format_rule(rule: Rule) -> str:
    return f"**{rule.rule_id}** - {rule.content}"


async def get_mute_role(guild_id: int) -> Optional[MuteRole]:
    return await MuteRole.get_or_none(server_id=guild_id)


async def create_mute_role(guild_id: int, role_id: int) -> MuteRole:
    role_row = await MuteRole()

    role_row.server_id = guild_id  # type: ignore
    role_row.role_id = role_id  # type: ignore

    await role_row.save()

    return role_row
