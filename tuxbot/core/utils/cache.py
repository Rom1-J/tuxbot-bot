import inspect
import time
from typing import Dict, Callable, Any, Optional, Union


class CacheItem:
    output: Optional[Any] = None

    def __init__(
        self,
        function: Callable,
        ttl: float = 10,
        args: tuple = (),
        kwargs: dict = None,
    ):
        if not kwargs:
            kwargs = {}

        self.function: Callable = function
        self.args: tuple = args
        self.kwargs: dict = kwargs

        self.expire_at: float = time.time() + ttl

        self.hits = 0
        self.misses = 0

    def expired(self, strict: bool) -> bool:
        if has_expired := ((time.time() > self.expire_at) or strict):
            self.misses += 1

        return has_expired

    # =========================================================================

    def get(self, strict: bool = False) -> Any:
        if not self.output or self.expired(strict):
            self.output = self.function(*self.args, **self.kwargs)
        else:
            self.hits += 1

        return self.output

    # =========================================================================

    async def async_get(self, strict: bool = False) -> Any:
        if not self.output or self.expired(strict):
            self.output = await self.function(*self.args, **self.kwargs)
        else:
            self.hits += 1

        return self.output


class Cache:
    def __init__(self):
        self.store: Dict[str, CacheItem] = {}

    @staticmethod
    def gen_key(*args, **kwargs):
        frame = inspect.stack()[1]

        base_key = f"{frame.filename}>{frame.function}"
        params = ""

        if args:
            params = ",".join([repr(arg) for arg in args])

        if kwargs:
            params += ",".join([f"{k}={repr(v)}" for k, v in kwargs.items()])

        return f"{base_key}({params})"

    # =========================================================================
    # =========================================================================

    def status(self, key: str) -> Optional[Dict[str, Union[int, float]]]:
        if key not in self.store:
            return None

        data = self.store[key]

        return {
            "expire_at": data.expire_at,
            "hits": data.hits,
            "misses": data.misses,
        }

    # =========================================================================

    def get(
        self,
        key: str,
        function: Callable,
        ttl: float = 3600,
        strict: bool = False,
        args: tuple = (),
        kwargs: Optional[dict] = None,
    ) -> Any:
        if key not in self.store:
            self.store[key] = CacheItem(
                function, ttl, args=args, kwargs=kwargs
            )

        return self.store[key].get(strict)

    # =========================================================================

    async def async_get(
        self,
        key: str,
        function: Callable,
        ttl: float = 3600,
        strict: bool = False,
        args: tuple = (),
        kwargs: Optional[dict] = None,
    ) -> Any:
        if key not in self.store:
            self.store[key] = CacheItem(
                function, ttl, args=args, kwargs=kwargs
            )

        return await self.store[key].async_get(strict)

    # =========================================================================
    # =========================================================================

    def __len__(self):
        return len(self.store)

    def __iter__(self):
        return iter(self.store)
