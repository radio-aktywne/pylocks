import asyncio
from abc import ABC, abstractmethod

import pytest

from pylocks.base import Lock


class LockLifespan(ABC):
    """Base class for managing the lifespan of a lock."""

    async def __aenter__(self) -> Lock:
        return await self.enter()

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.exit()

    @abstractmethod
    async def enter(self) -> Lock:
        """Enter the lifespan of the lock."""

        pass

    @abstractmethod
    async def exit(self) -> None:
        """Exit the lifespan of the lock."""

        pass


class LockLifespanBuilder(ABC):
    """Base class for building a lock lifespan."""

    @abstractmethod
    async def build(self) -> LockLifespan:
        """Build a lock lifespan."""

        pass


class BaseLockTest(ABC):
    """Base class for testing a lock."""

    @pytest.fixture
    @abstractmethod
    def builder(self) -> LockLifespanBuilder:
        """Return a builder for a lock lifespan."""

        pass

    @pytest.mark.asyncio(loop_scope="session")
    async def test_acquire_release(self, builder: LockLifespanBuilder) -> None:
        """Test that a lock can be acquired and released."""

        async with await builder.build() as lock:
            await lock.acquire()
            await lock.release()
            await lock.acquire()
            await lock.release()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_context_manager(self, builder: LockLifespanBuilder) -> None:
        """Test that a lock can be used as a context manager."""

        async with await builder.build() as lock:
            async with lock:
                pass

    @pytest.mark.asyncio(loop_scope="session")
    async def test_waits_when_locked(self, builder: LockLifespanBuilder) -> None:
        """Test that a lock waits when locked."""

        tried_by_first = asyncio.Event()
        tried_by_second = asyncio.Event()

        acquired_by_first = asyncio.Event()
        acquired_by_second = asyncio.Event()

        released_by_first = asyncio.Event()
        released_by_second = asyncio.Event()

        first_allowed_to_acquire = asyncio.Event()
        second_allowed_to_acquire = asyncio.Event()

        first_allowed_to_release = asyncio.Event()
        second_allowed_to_release = asyncio.Event()

        async def acquire_first(lock: Lock) -> None:
            await first_allowed_to_acquire.wait()

            tried_by_first.set()

            async with lock:
                acquired_by_first.set()

                await first_allowed_to_release.wait()

            released_by_first.set()

        async def acquire_second(lock: Lock) -> None:
            await second_allowed_to_acquire.wait()

            tried_by_second.set()

            async with lock:
                acquired_by_second.set()

                await second_allowed_to_release.wait()

            released_by_second.set()

        async with await builder.build() as lock:
            first = asyncio.create_task(acquire_first(lock))
            second = asyncio.create_task(acquire_second(lock))

            assert not acquired_by_first.is_set()
            assert not released_by_first.is_set()
            assert not acquired_by_second.is_set()
            assert not released_by_second.is_set()

            first_allowed_to_acquire.set()
            await tried_by_first.wait()
            await acquired_by_first.wait()

            assert acquired_by_first.is_set()
            assert not released_by_first.is_set()
            assert not acquired_by_second.is_set()
            assert not released_by_second.is_set()

            second_allowed_to_acquire.set()
            await tried_by_second.wait()

            assert acquired_by_first.is_set()
            assert not released_by_first.is_set()
            assert not acquired_by_second.is_set()
            assert not released_by_second.is_set()

            first_allowed_to_release.set()
            await released_by_first.wait()
            await acquired_by_second.wait()

            assert acquired_by_first.is_set()
            assert released_by_first.is_set()
            assert acquired_by_second.is_set()
            assert not released_by_second.is_set()

            second_allowed_to_release.set()
            await released_by_second.wait()

            assert acquired_by_first.is_set()
            assert released_by_first.is_set()
            assert acquired_by_second.is_set()
            assert released_by_second.is_set()

            await first
            await second
