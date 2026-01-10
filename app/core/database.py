from pymongo import MongoClient
import boto3
from botocore.client import Config
from app.core.config import settings

mongo_client = MongoClient(settings.MONGO_URL)
db = mongo_client[settings.DB_NAME]
media_collection = db["media"]

s3_client = boto3.client(
    's3',
    endpoint_url=settings.S3_ENDPOINT,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name=settings.S3_REGION
)

def ensure_bucket_exists():
    """Helper to create bucket if not exists"""
    try:
        s3_client.create_bucket(Bucket=settings.S3_BUCKET)
    except Exception:
        pass 