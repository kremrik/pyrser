def reader(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines = f.readlines()
    return lines
