import io
import boto3
from boto3 import client
from botocore.client import Config
import logging
from src.config import (
    MINIO_ENDPOINT,
    ACCESS_KEY,
    SECRET_KEY,
    BUCKET_NAME,
    REGION_NAME,
    SIGNATURE_VERSION,
)

logger = logging.getLogger(__name__)


class MinioClient:
    MINIO_ENDPOINT = MINIO_ENDPOINT
    ACCESS_KEY = ACCESS_KEY
    SECRET_KEY = SECRET_KEY
    BUCKET_NAME = BUCKET_NAME
    REGION_NAME = REGION_NAME
    SIGNATURE_VERSION = SIGNATURE_VERSION

    def __init__(
        self,
        endpoint=None,
        access_key=None,
        secret_key=None,
        bucket_name=None,
        region_name=None,
        signature_version=None,
    ):
        self.endpoint_url = endpoint or self.MINIO_ENDPOINT
        self.access_key = access_key or self.ACCESS_KEY
        self.secret_key = secret_key or self.SECRET_KEY
        self.bucket_name = bucket_name or self.BUCKET_NAME
        self.region_name = region_name or self.REGION_NAME
        self.signature_version = signature_version or self.SIGNATURE_VERSION

        self.s3: client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version=self.signature_version),
            region_name=self.region_name,
        )

    def bucket_exists(self) -> bool:
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception:
            return False

    def create_bucket(self) -> None:
        if not self.bucket_exists():
            try:
                self.s3.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": self.region_name},
                )
                logger.info(f"Bucket {self.bucket_name} created successfully.")
            except Exception as e:
                logger.error(f"Failed to create bucket {self.bucket_name}: {e}")
                raise

    def upload_fileobj(self, fileobj, object_name: str) -> None:
        if not self.bucket_exists():
            logger.info(f"Bucket {self.bucket_name} does not exist. Creating it.")
            self.create_bucket()
        self.s3.upload_fileobj(fileobj, self.bucket_name, object_name)
        logger.info(f"Uploaded {object_name} to bucket {self.bucket_name}.")

    def get_fileobj_in_memory(self, object_name: str) -> io.BytesIO:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
        return io.BytesIO(response["Body"].read())
