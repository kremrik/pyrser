from Node import Node, DirNode, FileNode, ClsNode, FncNode
from utils.file_utils import reader
from utils.regex import get_fnc_name
import ntpath


def pyrser(path: str) -> Node:
    if is_file(path):
        name = ntpath.basename(path)
        filenode_seed = FileNode(path, name)

        lines = reader(path)
        length = len(lines) - 1
        output = file_parser(FileNode, path, name, lines, length)

        # output.scope = [1, len(lines)]

        return output


def is_file(path: str) -> bool:
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    return ntpath.isfile(path)


place = 0

def file_parser(node: Node, location: str, name: str, lines: list, length: int, level: int = 0) -> Node:
    global place

    node = node(location, name)
    new_node = None
    scope_bgn = None
    scope_end = None

    while place <= length:
        this_line = lines[place]
        this_is_fnc = get_fnc_name(this_line)
        this_level = this_line.count("    ")

        next_line = None if place >= length else lines[place + 1]  # end of file
        next_is_fnc = None if next_line is None else get_fnc_name(next_line)
        next_level = level if next_is_fnc is None else next_line.count("    ")

        place += 1

        if (next_level <= level and next_is_fnc) or next_line is None:
            return node
        elif this_is_fnc:
            node.add_child(file_parser(FncNode, location, this_is_fnc, lines, length, level+1))
        else:
            continue

    return node
