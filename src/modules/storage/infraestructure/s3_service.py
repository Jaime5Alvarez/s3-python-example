import boto3
import asyncio
from modules.storage.domain.interfaces import IStorageService


class S3Service(IStorageService):
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3_client = boto3.client("s3", region_name=self.region_name, endpoint_url="http://localhost:4566")

    async def get_temp_url(self, key: str, expiration: int = 3600) -> str:
        """
        Generate a temporary URL for accessing an S3 object

        Args:
            key: The S3 object key
            expiration: URL expiration time in seconds (default: 1 hour)

        Returns:
            Temporary URL string
        """
        try:
            return await asyncio.to_thread(
                self.s3_client.generate_presigned_url,
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expiration,
            )
        except Exception as e:
            raise Exception(f"Error generating temporary URL: {str(e)}")

    async def get_item(self, key: str) -> bytes:
        """
        Retrieve an item from S3

        Args:
            key: The S3 object key

        Returns:
            The object content as bytes
        """
        try:
    
            response = await asyncio.to_thread(
                self.s3_client.get_object, Bucket=self.bucket_name, Key=key
            )
            return await asyncio.to_thread(response["Body"].read)
        except Exception as e:
            raise Exception(f"Error retrieving object: {str(e)}")

    async def set_item(self, key: str, value: bytes) -> None:
        """
        Store an item in S3

        Args:
            key: The S3 object key
            value: The content to store as bytes
        """
        try:
            await asyncio.to_thread(
                self.s3_client.put_object, Bucket=self.bucket_name, Key=key, Body=value
            )
        except Exception as e:
            raise Exception(f"Error storing object: {str(e)}")

    async def remove_item(self, key: str) -> None:
        """
        Remove an item from S3

        Args:
            key: The S3 object key
        """
        try:
            await asyncio.to_thread(
                self.s3_client.delete_object, Bucket=self.bucket_name, Key=key
            )
        except Exception as e:
            raise Exception(f"Error removing object: {str(e)}")

    async def create_bucket_if_not_exists(self) -> None:
        """
        Create the S3 bucket if it doesn't exist
        """
        try:
            await asyncio.to_thread(
                self.s3_client.head_bucket, Bucket=self.bucket_name
            )
        except Exception:
            # Bucket doesn't exist, create it
            if self.region_name == "us-east-1":
                # us-east-1 doesn't need LocationConstraint
                await asyncio.to_thread(
                    self.s3_client.create_bucket,
                    Bucket=self.bucket_name
                )
            else:
                await asyncio.to_thread(
                    self.s3_client.create_bucket,
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region_name}
                )

    async def clear_bucket(self) -> None:
        """
        Remove all objects from the S3 bucket
        """
        try:
            # List all objects in the bucket
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name)
            
            for page in pages:
                if 'Contents' in page:
                    objects_to_delete = [{'Key': obj['Key']} for obj in page['Contents']]
                    if objects_to_delete:
                        await asyncio.to_thread(
                            self.s3_client.delete_objects,
                            Bucket=self.bucket_name,
                            Delete={'Objects': objects_to_delete}
                        )
        except Exception as e:
            raise Exception(f"Error clearing bucket: {str(e)}")
