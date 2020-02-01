from Utils.Blacklisted import line_blacklisted
import os
from typing import List


def reader(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines = f.readlines()
    return lines


def join_path(path: str, filename: str) -> str:
    return os.path.join(path, filename)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def is_dir(path: str) -> bool:
    if line_blacklisted(path):
        return False
        
    return os.path.isdir(path)


def list_dir(path: str):
    for f in os.listdir(path):
        yield(os.path.join(path, f))


def nonempty_pyfile(path: str) -> bool:
    if line_blacklisted(path):
        return False

    return path.endswith(".py") and os.path.getsize(path) > 0


def get_file_name_from_path(path: str) -> str:
    return os.path.basename(path)


def get_parent_dir(path: str) -> str:
    return os.path.dirname(path)


def get_sibling_files(path: str) -> List[str]:
    return [f for f in os.listdir(path) if f.endswith(".py")]


def get_host_file(sibling_files: List[str], name: str) -> str:
    """returns the filepath of the file with a name like `name`"""
    return [f for f in sibling_files if name in f][0]
