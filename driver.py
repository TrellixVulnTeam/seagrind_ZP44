import re
import requests

STARTS = ["https://", "ftps://", "http://", "ftp://"]
ENDS = ["\\.zip", "tar\\.gz", "tar\\.bz2"]


def either_of(item):
    if isinstance(item, str):
        return item
    assert isinstance(item, list)
    if len(item) == 1:
        return item[0]
    return f"(?:{item[0]}|{either_of(item[1:])})"


def get_matches(text, startswith, endswith):
    startswith = either_of(startswith)
    endswith = either_of(endswith)
    matches = re.findall(f"{startswith}.*?{endswith}", text)
    return list(set(matches))


if __name__ == '__main__':
    html = """
    <!DOCTYPE html>
    <html>
        <body>
            <a href="https://github.com/org/repo/releases/download/version/file.tar.gz">Latest release</a>
            <a href="https://github.com/org/repo/releases/download/version/old.tar.gz">Previous release</a>
        </body>
    </html>
    """
    print(get_matches(html, STARTS, ENDS))