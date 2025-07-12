import pytest
import pytest_asyncio
from typing import AsyncGenerator
from modules.storage.infraestructure.s3_service import S3Service
from modules.storage.application.use_cases import (
    GetTempUrlUseCase,
    GetItemUseCase,
    SetItemUseCase,
    RemoveItemUseCase,
)


class StorageTestBuilder:
    def __init__(self):
        self.storage_service = S3Service(
            bucket_name="test-bucket", region_name="us-east-1"
        )
        # Inicializar casos de uso
        self.get_temp_url_use_case = GetTempUrlUseCase(self.storage_service)
        self.get_item_use_case = GetItemUseCase(self.storage_service)
        self.set_item_use_case = SetItemUseCase(self.storage_service)
        self.remove_item_use_case = RemoveItemUseCase(self.storage_service)


@pytest_asyncio.fixture
async def test_builder() -> AsyncGenerator[StorageTestBuilder, None]:
    builder = StorageTestBuilder()
    
    # Crear el bucket de S3 si no existe
    await builder.storage_service.create_bucket_if_not_exists()
    
    yield builder
    
    # Limpiar el bucket después de cada test
    await builder.storage_service.clear_bucket()


@pytest.mark.asyncio
async def test_set_item(test_builder):
    """Test para el caso de uso SetItem"""

    await test_builder.set_item_use_case.execute("test-key", b"test-value")

    result = await test_builder.get_item_use_case.execute("test-key")
    assert result == b"test-value"

    await test_builder.remove_item_use_case.execute("test-key")
    


@pytest.mark.asyncio
async def test_get_item(test_builder):
    """Test para el caso de uso GetItem"""
    # Primero almacenar un item
    test_key = "test-get-key"
    test_value = b"test-get-value"
    await test_builder.set_item_use_case.execute(test_key, test_value)

    # Luego recuperarlo
    result = await test_builder.get_item_use_case.execute(test_key)
    assert result == test_value


@pytest.mark.asyncio
async def test_remove_item(test_builder):
    """Test para el caso de uso RemoveItem"""
    # Primero almacenar un item
    test_key = "test-remove-key"
    test_value = b"test-remove-value"
    await test_builder.set_item_use_case.execute(test_key, test_value)

    # Luego eliminarlo
    await test_builder.remove_item_use_case.execute(test_key)
    
    # Verify that the item no longer exists
    with pytest.raises(Exception) as exc_info:
        await test_builder.get_item_use_case.execute(test_key)
    assert "NoSuchKey" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_temp_url(test_builder):
    """Test para el caso de uso GetTempUrl"""
    # Primero almacenar un item
    test_key = "test-url-key"
    test_value = b"test-url-value"
    await test_builder.set_item_use_case.execute(test_key, test_value)

    # Luego generar URL temporal
    temp_url = await test_builder.get_temp_url_use_case.execute(test_key)
    assert isinstance(temp_url, str)
    assert len(temp_url) > 0
