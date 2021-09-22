from discord.ext import menus  # type: ignore


class UserPageSource(menus.ListPageSource):
    def __init__(self, entries):
        super().__init__(entries=entries, per_page=1)

    # pylint: disable=arguments-differ, arguments-renamed
    async def format_page(self, menu, user):
        return user
