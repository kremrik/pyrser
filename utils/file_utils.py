def reader(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines = [line for line in f.readlines() if line != "\n"]
    return lines
