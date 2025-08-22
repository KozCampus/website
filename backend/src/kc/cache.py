from __future__ import annotations

import inspect
import typing as t
from functools import wraps

__all__ = ["lru_cache", "CacheInfo"]


T = t.TypeVar("T")
P = t.ParamSpec("P")


def lru_cache(maxsize: int):
    """
    Re-implementation of functools.lru_cache with proper type hints and async support.
    """
    def decorator(func: t.Callable[P, T]) -> t.Callable[P, T]:
        if inspect.iscoroutinefunction(func):
            return wraps(func)(LRUCacheAsyncFunctionWrapper(func, maxsize)) # type: ignore
        else:
            return wraps(func)(LRUCacheFunctionWrapper(func, maxsize))

    return decorator


class CacheInfo(t.NamedTuple):
    hits: int
    misses: int
    maxsize: int
    currsize: int


class LRUCache(t.Generic[T]):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.__cache: t.OrderedDict[t.Hashable, T] = t.OrderedDict()

    def get(self, key: t.Hashable) -> T | None:
        if key not in self.__cache:
            return None
        self.__cache.move_to_end(key)
        return self.__cache[key]

    def insert(self, key: t.Hashable, value: T) -> None:
        if len(self.__cache) == self.capacity:
            self.__cache.popitem(last=False)
        self.__cache[key] = value
        self.__cache.move_to_end(key)

    def __len__(self) -> int:
        return len(self.__cache)

    def clear(self) -> None:
        self.__cache.clear()


class LRUCacheFunctionWrapperBase(t.Generic[P, T]):
    def __init__(self, maxsize: int):
        self._cache = LRUCache[T](capacity=maxsize)
        self._hits = 0
        self._misses = 0
        self._maxsize: t.Final = maxsize


    def cache_info(self) -> CacheInfo:
        return CacheInfo(
            hits=self._hits,
            misses=self._misses,
            currsize=len(self._cache),
            maxsize=self._maxsize,
        )

    def cache_clear(self) -> None:
        self._cache.clear()
        self._hits = 0
        self._misses = 0


class LRUCacheFunctionWrapper(LRUCacheFunctionWrapperBase[P, T]):
    def __init__(self, func: t.Callable[P, T], maxsize: int):
        super().__init__(maxsize)
        self.__wrapped__ = func


    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        def wrapper():
            call_args = args + tuple(kwargs.items())

            ret = self._cache.get(call_args)

            if ret is None:
                self._misses += 1
                ret = self.__wrapped__(*args, **kwargs)
                self._cache.insert(call_args, ret)
            else:
                self._hits += 1

            return ret

        return wrapper()


class LRUCacheAsyncFunctionWrapper(LRUCacheFunctionWrapperBase[P, T]):
    def __init__(self, func: t.Callable[P, t.Awaitable[T]], maxsize: int):
        super().__init__(maxsize)
        self.__wrapped__ = func


    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> t.Awaitable[T]:
        async def wrapper():
            call_args = args + tuple(kwargs.items())

            ret = self._cache.get(call_args)

            if ret is None:
                self._misses += 1
                ret = await self.__wrapped__(*args, **kwargs)
                self._cache.insert(call_args, ret)
            else:
                self._hits += 1

            return ret

        coro = wrapper()
        return coro
