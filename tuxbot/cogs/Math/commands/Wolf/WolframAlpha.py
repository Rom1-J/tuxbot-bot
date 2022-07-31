"""
tuxbot.cogs.Math.commands.Wolf.WolframAlpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WolframAlpha api client
"""
import asyncio
import io

import aiohttp
import wolframalpha
from PIL import Image, ImageDraw, ImageFont


FONT = ImageFont.truetype(
    "./tuxbot/cogs/Math/commands/Wolf/fonts/DejaVuSans.ttf", size=16
)


class WolframAlpha:
    """WolframAlpha api"""

    client: wolframalpha.Client = None

    def __init__(self, api_key: str):
        self.loop = asyncio.get_running_loop()
        self.api_key = api_key

    async def get_client(self):
        """Retrieve client if not already done"""

        if self.client is None:

            def _get_client():
                return wolframalpha.Client(self.api_key)

            self.client = await self.loop.run_in_executor(None, _get_client)

    async def query(
        self, query: str
    ) -> tuple[str, wolframalpha.Result | None]:
        """Get query result from WolframAlpha"""

        def _query():
            return self.client.query(query)

        result: wolframalpha.Result = await self.loop.run_in_executor(
            None, _query
        )

        if result.success:
            return query, result

        if not hasattr(result, "didyoumean"):
            return query, None

        if isinstance(didyoumeans := result.didyoumeans["didyoumean"], list):
            query = didyoumeans[0]["#text"]
        else:
            query = didyoumeans["#text"]

        return await self.query(query)

    @staticmethod
    async def get_image(link) -> io.BytesIO | None:
        """Get image result from query link"""

        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=5)
            ) as cs, cs.get(link) as s:
                if s.status != 200:
                    return None

                return io.BytesIO(await s.read())
        except asyncio.exceptions.TimeoutError:
            from ...images.load_fail import value

            return io.BytesIO(value)

    @staticmethod
    async def get_images(
        result: wolframalpha.Result,
    ) -> dict[str, list[io.BytesIO | None]]:
        """Get image result from query result"""

        output: dict[str, list[io.BytesIO | None]] = {}

        for pod in result.pods:
            output[pod["@title"]] = []

            for subpod in pod.subpods:
                output[pod["@title"]].append(
                    await WolframAlpha.get_image(subpod.img.src)
                )

        return output

    async def merge_images(
        self, images: dict[str, list[io.BytesIO | None]], width: int
    ) -> io.BytesIO:
        """Merge all images as single one"""

        def _merge_images():
            height = self.height(images)

            background = Image.new(
                "RGB", (width + 30, height + 15), (255, 255, 255)
            )
            background_editable = ImageDraw.Draw(background)

            w, h = 15, 15

            for k, v in images.items():
                background_editable.text((w, h), k, (103, 142, 156), font=FONT)
                h += FONT.getsize(k)[1] + 10

                for image in v:
                    im = Image.open(image)
                    background.paste(im, (w, h))

                    h += im.size[1]

                h += 15

            buff = io.BytesIO()
            background.save(buff, "JPEG")

            return io.BytesIO(buff.getvalue())

        return await self.loop.run_in_executor(None, _merge_images)

    @staticmethod
    def width(result: wolframalpha.Result) -> int:
        """Get the highest image width"""

        def width_pod(pod):
            """Get width of actual pod"""
            return pod.img.width

        width = width_pod(
            max(
                max(
                    result.pods,
                    key=lambda pod: width_pod(max(pod.subpods, key=width_pod)),
                ).subpods,
                key=width_pod,
            )
        )

        return width if width >= 350 else 350

    @staticmethod
    def height(images: dict[str, list[io.BytesIO | None]]) -> int:
        """get height of all images"""

        height = 0

        for v in images.values():
            height += 42

            for image in v:
                if image:
                    img: Image = Image.open(image)
                    _, h = img.size

                    height += h

        return height

    @staticmethod
    def clean_query(query: str) -> str:
        """URL Encode for ?q="""

        query = query.replace("%", "%25")
        query = query.replace("(", "%28")
        query = query.replace(")", "%29")
        query = query.replace("+", "%2B")
        query = query.replace(" ", "+")

        return query
