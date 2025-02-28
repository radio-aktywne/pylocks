import pytest

from pylocks.asyncio import AsyncioLock
from tests.utils.unit import BaseLockTest, LockLifespan, LockLifespanBuilder


class AsyncioLockLifespan(LockLifespan):
    def __init__(self, lock: AsyncioLock) -> None:
        self._lock = lock

    async def enter(self) -> AsyncioLock:
        return self._lock

    async def exit(self) -> None:
        return None


class AsyncioLockLifespanBuilder(LockLifespanBuilder):
    async def build(self) -> AsyncioLockLifespan:
        return AsyncioLockLifespan(AsyncioLock())


class TestAsyncioLock(BaseLockTest):
    @pytest.fixture
    def builder(self) -> AsyncioLockLifespanBuilder:
        return AsyncioLockLifespanBuilder()
