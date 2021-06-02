import io
from typing import Optional

from sympy import preview


async def get_latex_bytes(loop, latex: str) -> Optional[io.BytesIO]:
    def _get_latex_bytes(_latex: str):
        buff = io.BytesIO()

        preview(_latex, viewer='BytesIO', outputbuffer=buff, euler=False,
                dvioptions=['-D', '1200'])

        return io.BytesIO(buff.getvalue())

    return await loop.run_in_executor(None, _get_latex_bytes, str(latex))
