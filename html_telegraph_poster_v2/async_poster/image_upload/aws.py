import asyncio
import os
import uuid
from datetime import datetime
from urllib.parse import urlparse, quote

import aiofiles.os
from pathlib import Path

import aioboto3
import httpx
from botocore.exceptions import ClientError

from html_telegraph_poster_v2.utils.logger import logger
from . import ImageUploader
from ..utils import download_file_to_local
from html_telegraph_poster_v2.config import AWS_S3_BUCKET_NAME, AWS_REGION_NAME, AWS_DOMAIN_HOST, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_S3_OBJECT_KEY
from ...utils.parse import check_url_is_local

image_url_host = (
    AWS_DOMAIN_HOST
    if AWS_DOMAIN_HOST
    else f"{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com"
)


class AWSUploader(ImageUploader):

    def __init__(self, access_key_id: str = AWS_ACCESS_KEY_ID, secret_access_key: str = AWS_SECRET_ACCESS_KEY,
                 region_name: str = AWS_REGION_NAME):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name

    async def upload_file(self, file_url: str, bucket_name: str = AWS_S3_BUCKET_NAME,
                          object_key: str = AWS_S3_OBJECT_KEY) -> str:
        # the object_key should be the directory path. We will append the file name to it
        if object_key.endswith("/"):
            object_key += Path(file_url).name
        else:
            object_key += "/" + Path(file_url).name

        if check_url_is_local(file_url):
            if not os.path.exists(file_url):
                raise FileNotFoundError(f"Local file '{file_url}' not found")
            with open(file_url, "rb") as file:
                content = file.read()
        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(file_url)
                response.raise_for_status()
                if response.status_code == 200:
                    content = response.content
                else:
                    logger.error(f"Failed to download {file_url}")
                    raise FileNotFoundError(f"Failed to download {file_url}")
        async with aioboto3.Session().client(
                "s3",
                region_name=self.region_name,
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
        ) as s3_client:
            try:
                response = await s3_client.put_object(
                    Bucket=bucket_name,
                    Key=object_key,
                    Body=content,
                )
                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    logger.info(f"Uploaded {file_url} to {bucket_name}/{object_key}")
                    return f"https://{image_url_host}/{object_key}"
                else:
                    logger.error(f"Failed to upload {file_url} to {bucket_name}/{object_key}")
                    return ""
            except ClientError as e:
                logger.error(f"Failed to upload {file_url} to {bucket_name}/{object_key}, {e}")
                return ""


async def download_and_upload(url: str, referer: str = None, suite: str = "test") -> str:
    urlparser = urlparse(url)
    file_name = (urlparser.netloc + urlparser.path).replace("/", "-")
    local_path = await download_file_to_local(url=url, referer=referer, file_name=file_name)
    local_path = Path(local_path)
    file_name = local_path.name
    if not local_path:
        return ""
    s3_path = await upload(
        suite=suite,
        staging_path=local_path,
        file_name=file_name,
    )
    await aiofiles.os.remove(local_path)
    return s3_path


async def upload(
        staging_path: Path,
        bucket: str = AWS_S3_BUCKET_NAME,
        suite: str = "test",
        release: str = datetime.now().strftime("%Y-%m-%d"),
        file_name: str = None,
) -> str:
    if not file_name:
        file_name = uuid.uuid4().hex
    blob_s3_key = f"{suite}/{release}/{file_name}"
    async with session.client("s3") as s3:
        try:
            with staging_path.open("rb") as spfp:
                logger.info(f"Uploading {blob_s3_key}")
                await s3.upload_fileobj(
                    spfp,
                    bucket,
                    blob_s3_key,
                )
                logger.info(f"Uploaded {file_name} to {suite}/{release}")
        except Exception as e:
            logger.error(f"Failed to upload {file_name} to {suite}/{release}, {e}")
            return ""
        image_url = f"https://{image_url_host}/{blob_s3_key}"
        urlparser = urlparse(image_url)
        quoted_url = urlparser.scheme + "://" + urlparser.netloc + quote(urlparser.path)
        return quoted_url
