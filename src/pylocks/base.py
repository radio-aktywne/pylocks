from abc import ABC, abstractmethod
from types import TracebackType


class Lock(ABC):
    """Base class for locks."""

    async def __aenter__(self) -> None:
        return await self.acquire()

    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return await self.release()

    @abstractmethod
    async def acquire(self) -> None:
        """Acquire the lock."""

    @abstractmethod
    async def release(self) -> None:
        """Release the lock."""
