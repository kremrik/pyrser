from Node import Node, DirNode, FileNode, ClsNode, FncNode
from utils.file_utils import reader
from utils.regex import get_fnc_name
import ntpath


name = "/home/kemri/Projects/pyrser/test_files/test1.py"


def pyrser(path: str) -> Node:
    if is_file(path):
        name = ntpath.basename(path)
        filenode_seed = FileNode(path, name)

        lines = reader(path)
        length = len(lines) - 1
        output = file_parser(filenode_seed, lines, length)

        output.scope = [1, len(lines)]

        return output


def is_file(path: str) -> bool:
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    return ntpath.isfile(path)


def file_parser(filenode: FileNode, lines: list, length: int, place: int = 0, level: int = 0) -> Node:
    # NOTE: level param is a measure of nesting to remain 0 in cases other than class methods
    # or nested functions (indicating a recursive call)

    new_node = None
    filename = filenode.location
    scope_bgn = None
    scope_end = None

    while place <= length:
        prev_line = None if place == 0 else lines[place - 1]
        this_line = lines[place]
        next_line = None if place >= length else lines[place + 1]
        prev_level = None if prev_line is None else prev_line.count("    ")
        this_level = this_line.count("    ")
        next_level = None if next_line is None else next_line.count("    ")  # add logic to ignore non-fnc indents

        place += 1

        # RETURN LOGIC
        # if the line after this is a function, we need to set the end scope for the function,
        # add the fnc_node as a child of the file_node, and then move to the next line
        next_line_fnc = get_fnc_name(next_line)
        if next_line is None or next_level <= level:  # short-circuit eval, 2nd expr can throw exception
            scope_end = place
            new_node.scope = [scope_bgn, scope_end]
            filenode.add_child(new_node)
            continue

        # SKIP LINE LOGIC
        # if this line isn't a function, we don't care about it
        fnc_name = get_fnc_name(this_line)
        if fnc_name is None:
            continue

        # CREATE NODE LOGIC
        # else, this line is a function so set the begin scope and make a new fnc_node
        if this_level == level:
            scope_bgn = place
            new_node = FncNode(filename, fnc_name)
            new_node.parent = filenode
        elif this_level > level:
            pass

    # once there are no more lines, we're done
    return filenode
