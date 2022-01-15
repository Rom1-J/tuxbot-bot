from tuxbot.core.utils.paginator import SimplePages


class TagPage:
    def __init__(self, entry):
        self.name = entry.name
        self.uses = entry.uses

    def __str__(self):
        return f"{self.name} ({self.uses})"


class TagPages(SimplePages):
    def __init__(self, entries, per_page=15):
        converted = [TagPage(entry) for entry in entries]

        super().__init__(converted, per_page=per_page)
