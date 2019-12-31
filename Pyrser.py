from Node import Node, DirNode, FileNode, ClsNode, FncNode
from utils.file_utils import reader
from utils.regex import get_fnc_name


name = "/home/kemri/Projects/pyrser/test_files/test1.py"


def pyrser(path: str) -> Node:
    lines = reader(path)
    length = len(lines) - 1
    output = run(name, lines, length)

    return output


def run(filename: str, lines: list, length: int, place: int = 0, level: int = 0) -> Node:
    """POC version of Pyrser that only works on a single file"""

    node = None
    scope_bgn = None
    scope_end = None

    while place <= length:
        this_line = lines[place]
        next_line = None if place >= length else lines[place + 1]
        next_level = None if next_line is None else next_line.count("    ")  # add logic to ignore non-fnc indents

        place += 1
        fnc_name = get_fnc_name(this_line)

        if fnc_name is None:
            continue

        node = FncNode(filename, fnc_name)
        scope_bgn = place

    scope_end = place - 1
    node.scope = [scope_bgn, scope_end]

    return node
