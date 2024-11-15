import base64
import os.path

import httpx

from html_telegraph_poster_v2.async_poster.image_upload.image_uploader import ImageUploader
from html_telegraph_poster_v2.config import GITHUB_REPO, GITHUB_BRANCH, GITHUB_PATH, GITHUB_COMMIT_MESSAGE
from html_telegraph_poster_v2.utils.logger import logger
from html_telegraph_poster_v2.utils.parse import check_url_is_local


class GithubUploader(ImageUploader):
    def __init__(self, token: str):
        self.token = token

    async def upload_file(self, file_url: str, repo: str = GITHUB_REPO, branch: str = GITHUB_BRANCH,
                          path: str = GITHUB_PATH, message: str = GITHUB_COMMIT_MESSAGE) -> str:
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        async with httpx.AsyncClient() as client:
            if check_url_is_local(file_url):
                if not os.path.exists(file_url):
                    logger.error(f"File {file_url} does not exist")
                    raise FileNotFoundError(f"File {file_url} does not exist")
                with open(file_url, "rb") as f:
                    content = base64.b64encode(f.read()).decode("utf-8")
            else:
                response = await client.get(file_url)
                response.raise_for_status()
                content = base64.b64encode(response.content).decode("utf-8")
            data = {
                "message": message,
                "content": content,
                "branch": branch,
            }
            response = await client.put(
                url=url,
                headers=headers,
                json=data,
            )
            if response.status_code == 201:
                logger.info(f"Uploaded {file_url} to {repo}/{path}")
                return response.json()["content"]["download_url"]
            else:
                logger.error(f"Failed to upload {file_url} to {repo}/{path}, {response.text}")
                return ""
