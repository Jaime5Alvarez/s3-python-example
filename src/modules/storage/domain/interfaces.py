from abc import ABC, abstractmethod


class IStorageService(ABC):
    @abstractmethod
    async def get_temp_url(self, key: str, expiration: int = 3600) -> str:
        pass

    @abstractmethod
    async def get_item(self, key: str) -> bytes:
        pass

    @abstractmethod
    async def set_item(self, key: str, value: bytes) -> None:
        pass

    @abstractmethod
    async def remove_item(self, key: str) -> None:
        pass
