from tuxbot.core.utils.Paginator.SimplePages import SimplePages


class TagPage:
    """One page of tags"""

    def __init__(self, i: int, entry):
        self.id: int = i
        self.name: str = entry.name
        self.uses: int = entry.uses

    def __str__(self):
        return f"{self.name} ({self.uses})"


class TagPages(SimplePages):
    """All tags pages"""

    def __init__(self, entries, ctx, per_page=15):
        super().__init__(
            [TagPage(i, entry) for i, entry in enumerate(entries)],
            ctx=ctx,
            per_page=per_page,
        )
