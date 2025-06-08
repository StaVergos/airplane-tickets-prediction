import boto3
from botocore.client import Config


class MinioClient:
    MINIO_ENDPOINT: str = "http://minio:9000"
    ACCESS_KEY: str = "minioadmin"
    SECRET_KEY: str = "minioadmin"
    BUCKET_NAME: str = "airplane-tickets"
    REGION_NAME: str = "us-east-1"
    SIGNATURE_VERSION: str = "s3v4"

    def __init__(
        self,
        endpoint: str = None,
        access_key: str = None,
        secret_key: str = None,
        bucket_name: str = None,
        region_name: str = None,
        signature_version: str = None,
    ):
        self.endpoint_url = endpoint or self.MINIO_ENDPOINT
        self.access_key = access_key or self.ACCESS_KEY
        self.secret_key = secret_key or self.SECRET_KEY
        self.bucket_name = bucket_name or self.BUCKET_NAME
        self.region_name = region_name or self.REGION_NAME
        self.signature_version = signature_version or self.SIGNATURE_VERSION

        self.s3 = self._create_s3_client()

    def _create_s3_client(self):
        return boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version=self.signature_version),
            region_name=self.region_name,
        )

    def create_bucket(self) -> dict:
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            return {}
        except Exception:
            response = self.s3.create_bucket(Bucket=self.bucket_name)
            return response

    def bucket_exists(self) -> bool:
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception:
            return False

    def upload_fileobj(self, fileobj, object_name: str) -> None:
        self.s3.upload_fileobj(fileobj, self.bucket_name, object_name)
