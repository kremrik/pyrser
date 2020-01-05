import ntpath


def reader(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines = [line for line in f.readlines() if line != "\n"]
    return lines


def is_file(path: str) -> bool:
    return ntpath.isfile(path)


def get_file_name_from_path(path: str) -> str:
    return ntpath.basename(path)
