import asyncio
from typing import Optional
from src.modules.storage.domain.interfaces import IStorageService


class GetTempUrlUseCase:
    
    def __init__(self, storage_service: IStorageService):
        self.storage_service = storage_service
    
    async def execute(self, key: str, expiration: int = 3600) -> str:

        return await self.storage_service.get_temp_url(key, expiration)


class GetItemUseCase:
    
    def __init__(self, storage_service: IStorageService):
        self.storage_service = storage_service
    
    async def execute(self, key: str) -> bytes:

        return await self.storage_service.get_item(key)


class SetItemUseCase:
    
    def __init__(self, storage_service: IStorageService):
        self.storage_service = storage_service
    
    async def execute(self, key: str, value: bytes) -> None:
 
        await self.storage_service.set_item(key, value)


class RemoveItemUseCase:
    
    def __init__(self, storage_service: IStorageService):
        self.storage_service = storage_service
    
    async def execute(self, key: str) -> None:

        await self.storage_service.remove_item(key) 