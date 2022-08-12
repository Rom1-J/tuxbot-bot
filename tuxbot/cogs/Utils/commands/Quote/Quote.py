import asyncio
import io
import textwrap

from PIL import Image, ImageDraw, ImageFont


FONT = ImageFont.truetype("DejaVuSans.ttf", size=32)
AUTHOR_FONT = ImageFont.truetype("DejaVuSans-Oblique.ttf", size=26)

PADDING = (42, 69)
QUOTES = ("“", "”")

BACKGROUND_COLOR = (22, 22, 22, 255)
TEXT_COLOR = (220, 220, 220, 255)


class Quote:
    text_width: int = 0
    text_height: int = 0

    def __init__(
        self, content: str, author: str, wrap_length: int = 50
    ) -> None:
        self.loop = asyncio.get_running_loop()

        self.content = QUOTES[0] + content + QUOTES[1]
        self.author = "– " + author

        self.wrap_length = wrap_length
        self.wrapped_content: list[str] = []

        self.wrap()
        self.get_size()

    def wrap(self) -> None:
        wrapper = textwrap.TextWrapper(width=self.wrap_length)
        self.wrapped_content = wrapper.wrap(text=self.content)

    def get_size(self) -> None:
        text_width, text_height = 0, 0

        for row in self.wrapped_content:
            row_width, row_height = FONT.getsize(row)

            text_height += row_height + 24

            if row_width > text_width:
                text_width = row_width

        self.text_width = text_width
        self.text_height = text_height

        if (
            author_width := AUTHOR_FONT.getsize(self.author)[0]
        ) > self.text_width:
            self.text_width = author_width + PADDING[0]

    async def generate(self) -> io.BytesIO:
        def _generate() -> io.BytesIO:
            background = Image.new(
                "RGBA",
                (
                    self.text_width + PADDING[0] * 2,
                    self.text_height + PADDING[1] * 2,
                ),
                BACKGROUND_COLOR,
            )
            background_editable = ImageDraw.Draw(background)

            background_editable.multiline_text(
                PADDING,
                "\n".join(self.wrapped_content),
                TEXT_COLOR,
                font=FONT,
                spacing=15,
            )

            author_width, author_height = FONT.getsize(self.author)
            background_editable.text(
                (
                    PADDING[0] + (self.text_width - author_width),
                    self.text_height + author_height + 24,
                ),
                self.author,
                TEXT_COLOR,
                font=AUTHOR_FONT,
            )

            buff = io.BytesIO()
            background.save(buff, "PNG")

            return io.BytesIO(buff.getvalue())

        return await self.loop.run_in_executor(None, _generate)
