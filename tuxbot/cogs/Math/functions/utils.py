import asyncio
import io
from typing import Optional, List, Dict, Tuple

import aiohttp
import wolframalpha

from sympy import preview
from sympy.printing.dot import dotprint
from graphviz import Source
from PIL import Image, ImageDraw, ImageFont

from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer


FONT = ImageFont.truetype("./tuxbot/cogs/Math/fonts/DejaVuSans.ttf", size=16)


class Wolfram:
    client: wolframalpha.Client = None

    def __init__(self, loop, api_key: str):
        self.loop = loop
        self.api_key = api_key

    async def get_client(self):
        if self.client is None:

            def _get_client():
                return wolframalpha.Client(self.api_key)

            self.client = await self.loop.run_in_executor(None, _get_client)

    @cached(
        ttl=24 * 3600,
        serializer=PickleSerializer(),
        cache=Cache.MEMORY,
        namespace="math",
    )
    async def query(
        self, query: str
    ) -> Tuple[str, Optional[wolframalpha.Result]]:
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
    @cached(
        ttl=24 * 3600,
        serializer=PickleSerializer(),
        cache=Cache.MEMORY,
        namespace="math",
    )
    async def get_image(link) -> Optional[io.BytesIO]:
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=5)
            ) as cs:
                async with cs.get(link) as s:
                    if s.status != 200:
                        return None

                    return io.BytesIO(await s.read())
        except asyncio.exceptions.TimeoutError:
            from ..images.load_fail import value

            return io.BytesIO(value)

    @cached(
        ttl=24 * 3600,
        serializer=PickleSerializer(),
        cache=Cache.MEMORY,
        namespace="math",
    )
    async def get_images(
        self, result: wolframalpha.Result
    ) -> Dict[str, List[Optional[io.BytesIO]]]:
        output: Dict[str, List[Optional[io.BytesIO]]] = {}

        for pod in result.pods:
            output[pod["@title"]] = []

            for subpod in pod.subpods:
                output[pod["@title"]].append(
                    await self.get_image(subpod.img.src)
                )

        return output

    @cached(
        ttl=24 * 3600,
        serializer=PickleSerializer(),
        cache=Cache.MEMORY,
        namespace="math",
    )
    async def merge_images(
        self, images: Dict[str, List[Optional[io.BytesIO]]], width: int
    ) -> io.BytesIO:
        height = self.height(images)

        background = Image.new(
            "RGBA", (width + 30, height + 15), (255, 255, 255, 255)
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
        background.save(buff, "PNG")

        return io.BytesIO(buff.getvalue())

    @staticmethod
    def width(result: wolframalpha.Result) -> int:
        # Function created on 7 June at 01:42 PM...
        def width_lambda(pod):
            return pod.img.width

        width = width_lambda(
            max(
                max(
                    result.pods,
                    key=lambda pod: width_lambda(
                        max(pod.subpods, key=width_lambda)
                    ),
                ).subpods,
                key=width_lambda,
            )
        )

        return width if width >= 350 else 350

    @staticmethod
    def height(images: Dict[str, List[Optional[io.BytesIO]]]) -> int:
        height = 0

        for v in images.values():
            height += 42

            for image in v:
                if image:
                    img: Image = Image.open(image)
                    _, h = img.size

                    height += h

        return height


async def get_latex_bytes(loop, latex: str) -> Optional[io.BytesIO]:
    def _get_latex_bytes(_latex: str):
        buff = io.BytesIO()

        preview(
            _latex,
            viewer="BytesIO",
            outputbuffer=buff,
            euler=False,
            dvioptions=["-D", "1200"],
        )

        return io.BytesIO(buff.getvalue())

    return await loop.run_in_executor(None, _get_latex_bytes, str(latex))


def clean_query(query: str) -> str:
    query = query.replace("%", "%25")
    query = query.replace("+", "%2B")
    query = query.replace(" ", "+")

    return query


async def get_graph_bytes(loop, expr) -> io.BytesIO:
    def _get_graph_bytes(_expr):
        digraph = dotprint(expr)
        raw_bytes = Source(digraph).pipe(format="png")

        return io.BytesIO(raw_bytes)

    return await loop.run_in_executor(None, _get_graph_bytes, expr)
