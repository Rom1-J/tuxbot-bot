import discord


class PlaylistSelect(discord.ui.Select):
    def __init__(
        self, options: list, author: discord.User, page=0, ephemeral=False
    ):
        self._page = page
        self._options = options

        self._author = author
        self._ephemeral = ephemeral

        super().__init__(
            placeholder=f"Page: {self._page + 1}/{len(self._options)}",
            min_values=1,
            max_values=1,
            options=self._options[self._page],
        )

    async def callback(self, interaction: discord.Interaction):

        if interaction.data["values"][0] == "more":
            return await self._update_page(interaction, +1)

        if interaction.data["values"][0] == "less":
            return await self._update_page(interaction, -1)

        await interaction.response.send_message(
            content="Not implemented yet", ephemeral=True
        )

    def _check_author(self, interaction: discord.Interaction):
        return interaction.user == self._author

    async def _update_page(self, interaction: discord.Interaction, page: int):
        view = discord.ui.View()

        if self._check_author(interaction):
            self._page += page
            self.placeholder = f"Page: {self._page + 1}/{len(self._options)}"

            self.options = self._options[self._page]

            view.add_item(self)
            await interaction.response.edit_message(
                content="Music on hold:", view=view
            )
        else:
            select = PlaylistSelect(
                self._options,
                interaction.user,
                page=self._page + page,
                ephemeral=True,
            )
            view.add_item(select)

            await interaction.response.send_message(
                content="Music on hold:", view=view, ephemeral=True
            )
