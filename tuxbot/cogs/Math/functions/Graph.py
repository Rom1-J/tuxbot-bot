import io

from graphviz import Source
from sympy import dotprint


async def get_graph_bytes(loop, expr) -> io.BytesIO:
    """Generate graph as byte format from given expr"""

    def _get_graph_bytes(_expr):
        digraph = dotprint(expr)
        raw_bytes = Source(digraph).pipe(format="png")

        return io.BytesIO(raw_bytes)

    return await loop.run_in_executor(None, _get_graph_bytes, expr)
