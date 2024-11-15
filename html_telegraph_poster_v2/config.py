import os
from typing import Optional

env = os.environ


def get_bool(value: Optional[str], default: bool = True) -> bool:
    true_values = ("True", "true", "1", "yes", "on")
    false_values = ("False", "false", "0", "no", "off")

    if value is None:
        return default
    value = value.lower()

    if value in true_values:
        return True
    elif value in false_values:
        return False
    else:
        return default


def get_env_bool(env, var_name: Optional[str], default: bool = False):
    """Retrieve environment variable as a boolean."""
    value = env.get(var_name, "").lower()
    return get_bool(value, default)


# General
DEFAULT_USER_AGENT = env.get("DEFAULT_USER_AGENT", "Python_html_telegraph_poster_v2/0.1")
DOWNLOAD_DIR = env.get("DOWNLOAD_DIR", os.path.join(os.getcwd(), "download"))

# Image Uploading
# AWS S3
AWS_ACCESS_KEY_ID = env.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = env.get("AWS_SECRET_ACCESS_KEY", None)
AWS_S3_BUCKET_NAME = env.get("AWS_S3_BUCKET_NAME", None)
AWS_REGION_NAME = env.get("AWS_REGION_NAME", None)
AWS_S3_OBJECT_KEY = env.get("AWS_OBJECT_KEY", None)
AWS_DOMAIN_HOST = env.get("AWS_DOMAIN_HOST", None)
# GitHub
GITHUB_TOKEN = env.get("GITHUB_TOKEN", None)
GITHUB_REPO = env.get("GITHUB_REPO", None)
GITHUB_BRANCH = env.get("GITHUB_BRANCH", None)
GITHUB_PATH = env.get("GITHUB_PATH", None)
GITHUB_COMMIT_MESSAGE = env.get("GITHUB_COMMIT_MESSAGE", None)