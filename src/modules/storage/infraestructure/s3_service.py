import boto3
import asyncio
from typing import Optional
from botocore.exceptions import ClientError, NoCredentialsError
from src.modules.storage.domain.interfaces import IStorageService


class S3Service(IStorageService):
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.region_name = region_name

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
            s3_client = boto3.client('s3', region_name=self.region_name)
            return await asyncio.to_thread(
                s3_client.generate_presigned_url,
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiration
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
            s3_client = boto3.client('s3', region_name=self.region_name)
            response = await asyncio.to_thread(
                s3_client.get_object,
                Bucket=self.bucket_name,
                Key=key
            )
            return await asyncio.to_thread(response['Body'].read)
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
            s3_client = boto3.client('s3', region_name=self.region_name)
            await asyncio.to_thread(
                s3_client.put_object,
                Bucket=self.bucket_name,
                Key=key,
                Body=value
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
            s3_client = boto3.client('s3', region_name=self.region_name)
            await asyncio.to_thread(
                s3_client.delete_object,
                Bucket=self.bucket_name,
                Key=key
            )
        except Exception as e:
            raise Exception(f"Error removing object: {str(e)}")