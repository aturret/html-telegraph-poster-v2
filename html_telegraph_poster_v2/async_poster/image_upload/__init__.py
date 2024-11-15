from .aws import AWSUploader
from .github import GithubUploader

uploader_list = {
    "aws": AWSUploader,
    "github": GithubUploader,
}
