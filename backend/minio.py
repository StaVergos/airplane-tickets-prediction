import boto3
from botocore.client import Config


class MinioClient:
    """
    A wrapper around boto3 client for MinIO operations.
    """

    MINIO_ENDPOINT: str = "http://localhost:9000"
    ACCESS_KEY: str = "minioadmin"
    SECRET_KEY: str = "minioadmin"
    BUCKET_NAME: str = "airplane-tickets"
    REGION_NAME: str = "us-east-1"  # Required by boto3 (ignored by MinIO)
    SIGNATURE_VERSION: str = "s3v4"

    def __init__(self):
        """
        Initialize the MinIO client using constants.
        """
        self.endpoint_url = self.MINIO_ENDPOINT
        self.access_key = self.ACCESS_KEY
        self.secret_key = self.SECRET_KEY
        self.bucket_name = self.BUCKET_NAME
        self.region_name = self.REGION_NAME
        self.signature_version = self.SIGNATURE_VERSION
        self.s3 = self._create_s3_client()

    def _create_s3_client(self):
        """
        Create and return a boto3 S3 client configured for MinIO.
        """
        return boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version=self.signature_version),
            region_name=self.region_name,
        )

    def create_bucket(self) -> dict:
        """
        Create the configured bucket if it does not already exist.

        :return: Response from create_bucket API or empty dict if it already exists
        """
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' already exists.")
            return {}
        except Exception:
            response = self.s3.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' created.")
            return response

    def bucket_exists(self) -> bool:
        """
        Check if the bucket exists.

        :return: True if the bucket exists, False otherwise
        """
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception:
            return False
        
