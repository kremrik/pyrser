from Node import Node, DirNode, FileNode, ClsNode, FncNode
from utils.file_utils import reader
from utils.regex import get_fnc_name
import ntpath


name = "/home/kemri/Projects/pyrser/test_files/test1.py"


def pyrser(path: str) -> Node:
    if is_file(path):
        name = ntpath.basename(path)
        filenode = FileNode(path, name)

        lines = reader(path)
        length = len(lines) - 1
        obj_node = file_parser(path, lines, length)

        print("LENGTH: {}".format(len(lines)))
        filenode.scope = [1, len(lines)]
        filenode.add_child(obj_node)

        return filenode


def is_file(path: str) -> bool:
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    return ntpath.isfile(path)


def file_parser(filename: str, lines: list, length: int, place: int = 0, level: int = 0) -> Node:
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

    scope_end = place
    node.scope = [scope_bgn, scope_end]

    return node
