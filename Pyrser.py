from Node import Node, DirNode, FileNode, ClsNode, FncNode
from utils.file_utils import reader, is_file, get_file_name_from_path
from utils.regex import get_obj_name


place = 0  # TODO: find a way to avoid this...
INDENT = "    "


def pyrser(path: str) -> Node:
    global place
    place = 0

    if is_file(path):
        name = get_file_name_from_path(path)
        filenode_seed = FileNode(path, name)

        lines = reader(path)
        length = len(lines) - 1
        output = file_parser(FileNode, path, name, lines, length)

        return output


def file_parser(node, location: str, name: str, lines: list, length: int, level: int = 0) -> Node:
    global place

    node = node(location, name)
    new_node = None
    scope_bgn = place if place > 0 else 1  # always want to start at line 1, not 0

    while place <= length:
        this_line = lines[place]
        this_is_fnc = get_obj_name(this_line)
        this_level = this_line.count(INDENT)

        next_line = None if place >= length else lines[place + 1]
        next_is_fnc = None if next_line is None else get_obj_name(next_line)
        next_level = level if next_is_fnc is None else next_line.count(INDENT)

        if next_is_fnc and next_level < level:
            # if we're in a nested definition, don't increment place (ie, move to the
            # next line) until we've returned out of enough recursive calls to make
            # the levels equal...
            node.scope = [scope_bgn, place+1]
            return node
        else:
            # ... THEN once they're equal, increment place/move on to the next line
            place += 1

        if next_line is None:
            node.scope = [scope_bgn, place]
            return node
        elif this_is_fnc:
            child = file_parser(FncNode, location, this_is_fnc, lines, length, level+1)
            child.parent = node
            node.add_child(child)
        else:
            # something other than a definition, which we don't care about yet
            # this is where we will add tracking for function calls, however
            continue
    
    node.scope = [scope_bgn, place or 1]
    return node
