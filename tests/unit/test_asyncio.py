from typing import override

import pytest

from pylocks.asyncio import AsyncioLock
from tests.utils.unit import BaseLockTest, LockLifespan, LockLifespanBuilder


class AsyncioLockLifespan(LockLifespan):
    """Lifespan for AsyncioLock."""

    def __init__(self, lock: AsyncioLock) -> None:
        self._lock = lock

    @override
    async def enter(self) -> AsyncioLock:
        return self._lock

    @override
    async def exit(self) -> None:
        return None


class AsyncioLockLifespanBuilder(LockLifespanBuilder):
    """Builder for AsyncioLockLifespan."""

    @override
    async def build(self) -> AsyncioLockLifespan:
        return AsyncioLockLifespan(AsyncioLock())


class TestAsyncioLock(BaseLockTest):
    """Tests for AsyncioLock."""

    @pytest.fixture
    @override
    def builder(self) -> AsyncioLockLifespanBuilder:
        return AsyncioLockLifespanBuilder()
