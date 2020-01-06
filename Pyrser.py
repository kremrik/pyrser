from Node import Node, DirNode, FileNode, ClsNode, FncNode
# from utils.file_utils import reader, is_file, get_file_name_from_path
from Helpers import reader, is_file, get_file_name_from_path, get_obj_name


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
    in_comment = False

    while place <= length:
        this_line = lines[place]
        this_is_fnc = get_obj_name(this_line)
        this_level = this_line.count(INDENT)

        next_line = None if place >= length else lines[place + 1]
        next_is_fnc = None if next_line is None else get_obj_name(next_line)
        next_level = level if next_is_fnc is None else next_line.count(INDENT)

        # recursive breakout logic
        if next_is_fnc and next_level < level:
            node.scope = [scope_bgn, place+1]
            return node
  
        place += 1

        # end-of-file logic
        if next_line is None:
            node.scope = [scope_bgn, place]
            return node

        # skip comment logic
        if '"""' in this_line:
            in_comment = not in_comment
            continue
        elif in_comment is True:
            continue
        elif this_line.strip().startswith("#"):
            continue

        # recurse logic
        if this_is_fnc:
            child = file_parser(FncNode, location, this_is_fnc, lines, length, level+1)
            child.parent = node
            node.add_child(child)

        # if no other conditions met, move on to the next line
        continue
    
    node.scope = [scope_bgn, place or 1]
    return node
