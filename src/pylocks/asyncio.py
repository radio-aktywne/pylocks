import asyncio
from typing import override

from pylocks.base import Lock


class AsyncioLock(Lock):
    """Asyncio lock."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

    @override
    async def acquire(self) -> None:
        await self._lock.acquire()

    @override
    async def release(self) -> None:
        self._lock.release()
