from urllib.parse import urlparse


def check_url_is_local(url: str) -> bool:
    return urlparse(url).netloc == ""
