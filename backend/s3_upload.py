import os
from datetime import datetime
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")


def get_s3_client():
    return boto3.client("s3", region_name=AWS_REGION)


def build_s3_key(prefix: str = "raw-logs/auth") -> str:
    now = datetime.utcnow()
    date_prefix = now.strftime("%Y/%m/%d")
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")
    filename = f"auth_logs_{timestamp}.jsonl"
    return f"{prefix}/{date_prefix}/{filename}"


def upload_auth_logs(file_path):

    if not S3_BUCKET:
        raise RuntimeError("S3_BUCKET_NAME is not set in environment or .env file.")

    file_path = Path(file_path)

    s3_key = build_s3_key()
    s3_client = get_s3_client()

    try:
        with open(file_path, "rb") as f:
            s3_client.upload_fileobj(f, S3_BUCKET, s3_key)

        print(f"Uploaded {file_path} to s3://{S3_BUCKET}/{s3_key}")

    except (BotoCoreError, ClientError) as e:
        print(f"Error uploading logs to S3: {e}")