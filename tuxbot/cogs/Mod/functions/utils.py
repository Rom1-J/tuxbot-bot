from tuxbot.cogs.Mod.models.rules import Rule
from tuxbot.core.config import set_for_key
from tuxbot.core.config import Config

from tuxbot.core.bot import Tux
from tuxbot.core.utils.functions.extra import ContextPlus


async def save_lang(bot: Tux, ctx: ContextPlus, lang: str) -> None:
    set_for_key(bot.config.Servers, ctx.guild.id, Config.Server, locale=lang)


async def get_server_rules(guild_id: int) -> list[Rule]:
    return await Rule.filter(server_id=guild_id).all()


def get_most_recent_server_rules(rules: list[Rule]) -> Rule:
    return sorted(rules, key=lambda r: r.updated_at, reverse=True)[0]


def paginate_server_rules(rules: list[Rule]) -> list[str]:
    body = [""]

    for rule in rules:
        if len(body[-1] + format_rule(rule)) > 2000:
            body.append(format_rule(rule) + "\n")
        else:
            body[-1] += format_rule(rule) + "\n"

    return body


def format_rule(rule: Rule) -> str:
    return f"**{rule.rule_id}** - {rule.content}"
