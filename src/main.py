from modules.storage.application.use_cases import SetItemUseCase
from modules.storage.infraestructure.s3_service import S3Service

import asyncio


async def main():
    set_item_use_case = SetItemUseCase(
        storage_service=S3Service(bucket_name="test-bucket", region_name="eu-south-2")
    )
    await set_item_use_case.execute("test-key", b"test-value")


if __name__ == "__main__":
    asyncio.run(main())
