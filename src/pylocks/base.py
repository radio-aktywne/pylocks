from abc import ABC, abstractmethod


class Lock(ABC):
    """Base class for locks."""

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.release()

    @abstractmethod
    async def acquire() -> None:
        """Acquire the lock."""

        pass

    @abstractmethod
    async def release() -> None:
        """Release the lock."""

        pass
