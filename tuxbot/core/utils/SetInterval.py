"""
Alternative for setInterval
"""
import asyncio
from contextlib import suppress


class SetInterval:
    """Python alternative of javascript setInterval

    source: https://stackoverflow.com/a/37514633
    """
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self):
        """Start the loop"""
        if not self.is_started:
            self.is_started = True

            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        """Stop the loop"""
        if self.is_started:
            self.is_started = False

            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            await asyncio.sleep(self.time)
            self.func()
