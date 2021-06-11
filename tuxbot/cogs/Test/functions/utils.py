from discord import ui


class Button(ui.Button):
    pass


class TicTacToe(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__()

        _ = args
        __ = kwargs
