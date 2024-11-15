from abc import ABC, abstractmethod

from .aws import AWSUploader
from .github import GithubUploader

uploader_list = {
    "aws": AWSUploader,
    "github": GithubUploader,
}


class ImageUploader:

    @abstractmethod
    async def upload_file(self, **kwargs) -> str:
        pass
