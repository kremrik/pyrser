from Node import Node, DirNode, FileNode, ClsNode, FncNode
from Utils.PyrserHelpers import reader, is_file, get_file_name_from_path, get_obj_name, \
    get_node_type, get_next_nonempty_line, xfs, get_fnc_calls


INDENT = "    "


def pyrser(path: str) -> Node:
    if is_file(path):
        name = get_file_name_from_path(path)
        filenode_seed = FileNode(path, name)

        lines = reader(path)
        length = len(lines) - 1
        output, _ = file_parser(FileNode, path, name, lines, length)

        return output


def file_parser(node, location: str, name: str, lines: list, length: int, place: int = 0, level: int = 0) -> Node:
    """
    The function that will parse a .py file and return the basic hierarchy of its functions and classes. 
    ``FncNode.calls`` functionality is added in a second stage.
    """

    node = node(location, name)
    new_node = None
    scope_bgn = place if place > 0 else 1  # always want to start at line 1, not 0
    in_comment = False

    while place <= length:
        this_line = lines[place]
        this_is_node = get_obj_name(this_line)
        this_level = this_line.count(INDENT)

        next_line = None if place >= length else get_next_nonempty_line(lines, place, length)
        next_is_node = None if next_line is None else get_obj_name(next_line)
        next_level = level if next_is_node is None else next_line.count(INDENT)

        # recursive breakout logic
        # do not want to increment place until levels at this and next line equal
        if next_is_node and next_level < level:
            node.scope = [scope_bgn, place+1]
            return node, place
  
        place += 1

        # end-of-file logic
        if next_line is None:
            node.scope = [scope_bgn, place]
            return node, place

        # skip comment logic
        if '"""' in this_line:
            in_comment = not in_comment
            continue
        elif in_comment or this_line.strip().startswith("#"):
            continue

        # recurse logic
        if this_is_node:
            this_node_type = get_node_type(this_line)
            child, new_place = file_parser(this_node_type, location, this_is_node, lines, length, place, level+1)
            child.parent = node
            place = new_place
            node.add_child(child)

        # if no other conditions met, move on to the next line
        continue
    
    node.scope = [scope_bgn, place or 1]
    return node, place


def add_calls(node: Node, lines: list) -> Node:
    filename = node.location

    for line in lines:
        if calls := get_fnc_calls(line):  # if this line calls function(s)
            for call in calls:
                if fnc := xfs(node=node, tgt_name=call, tgt_file=node.location) and type(fnc) == FncNode:
                    # get the function we're in
                    # add fnc to its `calls` attr
                    pass
