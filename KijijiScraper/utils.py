from ast import parse
from urllib.parse import urlparse


def format_string(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_splitted = path.split("/")
    prefix = "/".join(path_splitted[:-1])
    suffix = path_splitted[-1]
    url_prefix = f"{parsed_url.scheme}://{parsed_url.netloc}{prefix}"
    url_suffix = f"{suffix}?{parsed_url.query}"
    return url_prefix, url_suffix
