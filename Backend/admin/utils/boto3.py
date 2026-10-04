import boto3
import os
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from shared.errors.errors import S3UploadError

load_dotenv(override=True)
async def get_client():
    client =  boto3.client(
        service_name="s3",
        aws_secret_access_key= os.getenv("SECRET_KEY"),
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        endpoint_url=os.getenv("ENDPOINTS"),
    )
    return client

async def upload_to_s3(file,file_name,redis):
    try :
        client = await get_client()
        client.upload_fileobj(file,"etudiantia", file_name)
    except ClientError as e :
        raise S3UploadError(redis["upload"]["error"])