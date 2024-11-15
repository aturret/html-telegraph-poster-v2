from abc import abstractmethod


class ImageUploader:

    @abstractmethod
    async def upload_file(self, **kwargs) -> str:
        pass
