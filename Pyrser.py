from Node import Node, DirNode, FileNode, ClsNode, FncNode
import Utils.FileHelpers as fh
from Utils.PyrserHelpers import get_obj_name, get_node_type, get_next_nonempty_line, xfs, get_fnc_calls, get_fnc_from_line  # TODO: convert to alias
import ImportParser as ip


INDENT = "    "


def pyrser(path: str) -> Node:
    # TODO/BUG: can't call add_calls on single file for is_dir, need to
    # call on entire directory somehow

    if fh.is_dir(path):
        output_with_calls = dir_parser(path)

    if fh.is_file(path):
        name = fh.get_file_name_from_path(path)

        lines = fh.reader(path)
        length = len(lines) - 1
        output, _ = file_parser(FileNode, path, name, lines, length)  # TODO: eliminate useless second return value
        
        # output_with_calls = add_calls(output, lines)
        output_with_calls = output
        
    return output_with_calls


def dir_parser(path: str) -> Node:
    name = fh.get_file_name_from_path(path)
    dirnode = DirNode(path, name)

    for f in fh.list_dir(path):
        if fh.nonempty_pyfile(f):
            f_name = fh.get_file_name_from_path(f)
            lines = fh.reader(f)
            length = len(lines) - 1
            output, _ = file_parser(FileNode, f, f_name, lines, length)  # TODO: eliminate useless second return value

            # output_with_calls = add_calls(output, lines)
            output.parent = dirnode
            dirnode.add_child(output)

        if fh.is_dir(f):
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


def add_calls(graph: Node):
    """
    1. Scan graph for FileNode
    2. When FileNode found, open file
    3. Iterate through file line-by-line
        If function call found, use ``get_fnc_from_line`` to get its "home" function,
        and then query graph with ``xfs`` and tgt_nm and file_nm params
    4. query graph with name of function called in (3)
        If found, add to (3)'s "home" function node
        Else, pass
    """
    for node in [n for n in graph if type(n) == FileNode]:
        filepath = node.location
        lines = fh.reader(filepath)

        for place, line in enumerate(lines):
            if fnc_call := get_fnc_calls(line):  # if this line calls a function...
                # if fnc_call[0] == "dir_parser": print(f"fnc_call: {fnc_call}, line: {line.strip()}")
                if fnc_node := xfs(graph, tgt_nm=fnc_call[0]):  # if called function in graph...
                    # if fnc_call[0] == "dir_parser": print(f"fnc_node: {fnc_node}")
                    call_owner = get_fnc_from_line(lines, place)  # get the name of function calling fnc_node
                    # if fnc_call[0] == "dir_parser": print(f"call_owner: {call_owner}")
                    caller_node = xfs(graph, tgt_nm=call_owner)  # get the node of the function calling fnc_node
                    # if fnc_call[0] == "dir_parser": print(f"caller_node: {caller_node}")
                    if type(caller_node) == FncNode:
                        caller_node.add_call(fnc_node)
