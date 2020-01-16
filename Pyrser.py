from Node import Node, DirNode, FileNode, ClsNode, FncNode
from Utils.PyrserHelpers import reader, is_file, get_file_name_from_path, get_obj_name, \
    get_node_type, get_next_nonempty_line, xfs, get_fnc_calls, get_fnc_from_line, is_dir, \
    list_dir, nonempty_pyfile


INDENT = "    "


def pyrser(path: str) -> Node:
    if is_dir(path):
        output_with_calls = dir_parser(path)

    if is_file(path):
        name = get_file_name_from_path(path)

        lines = reader(path)
        length = len(lines) - 1
        output, _ = file_parser(FileNode, path, name, lines, length)  # TODO: eliminate useless second return value
        
        output_with_calls = add_calls(output, lines)
        
    return output_with_calls


def dir_parser(path: str) -> Node:
    name = get_file_name_from_path(path)
    dirnode = DirNode(path, name)

    for f in list_dir(path):
        if nonempty_pyfile(f):
            f_name = get_file_name_from_path(f)
            lines = reader(f)
            length = len(lines) - 1
            output, _ = file_parser(FileNode, f, f_name, lines, length)  # TODO: eliminate useless second return value

            output_with_calls = add_calls(output, lines)
            output.parent = dirnode
            dirnode.add_child(output)

        if is_dir(f):
            child_dir = dir_parser(f)
            child_dir.parent = dirnode
            dirnode.add_child(child_dir)

    return dirnode


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

    for place, line in enumerate(lines):
        if calls := get_fnc_calls(line):  # if this line calls function(s)
            for call in calls:  # there may be multiple functions called
                # if that fnc is defined in our Node AND it's a FncNode, add it as a call to 
                # whichever function called it
                if called_node := xfs(node=node, tgt_nm=call, tgt_file=node.location):
                    parent_fnc_name = get_fnc_from_line(lines, place)
                    parent_fnc = xfs(node=node, tgt_nm=parent_fnc_name, tgt_file=node.location)
                    parent_fnc.add_call(called_node)

    return node
