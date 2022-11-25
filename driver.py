import re
import requests
import platform
import os
import tarfile
import zipfile


class GECKOLINKS:
    baseurl = "https://github.com"
    prefix = "/mozilla/geckodriver/releases/download/"
    Linux = "linux64.tar.gz"
    Darwin = "macos.tar.gz"
    Windows = "win64.zip"


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


def filter_links(links, keywords):
    return next(filter(lambda link: all((key in link) for key in keywords), links))


def download_archive(url):
    resp = requests.get(url)
    archive = url.split('/')[-1]
    with open(archive, 'wb') as f:
        f.write(resp.content)
    return archive


def extract_archive(archive):
    if 'tar' in archive:
        with tarfile.open(archive) as f:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(f, "./driver/")
    if 'zip' in archive:
        with zipfile.ZipFile(archive, 'r') as f:
            f.extractall('./driver/')
    os.remove(archive)


def get_geckodriver():
    if os.path.exists('./driver/'):
        if any('geckodriver' in x for x in os.listdir('./driver/')):
            return None
    resp = requests.get("https://github.com/mozilla/geckodriver/releases/latest")
    html = resp.text
    links = get_matches(html,
                        [GECKOLINKS.prefix],
                        ["\\.zip", "tar\\.gz"])
    p = platform.system()
    ext_url = filter_links(links, getattr(GECKOLINKS, p))
    archive = download_archive(GECKOLINKS.baseurl + ext_url)
    extract_archive(archive)
