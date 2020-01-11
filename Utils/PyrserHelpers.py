from Node import Node, DirNode, FileNode, ClsNode, FncNode
from collections import deque, defaultdict
import ntpath


BLACKLIST_CHARS = ["__"]


def _line_blacklisted(line: str) -> bool:
    for chars in BLACKLIST_CHARS:
        if chars in line:
            return True
    return False


def reader(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines =f.readlines()
    return lines


def is_file(path: str) -> bool:
    return ntpath.isfile(path)


def get_file_name_from_path(path: str) -> str:
    return ntpath.basename(path)


def xfs(node: Node, tgt_nm: str = None, tgt_file: str = None, search_type: str = "dfs") -> Node:
    # TODO: could implement __hash__ for Node so we can use a set
    visited = []  
    stack = deque([node]) if search_type == "bfs" else [node]

    while stack:
        vertex = stack.pop()

        if tgt_nm and tgt_file:
            if vertex.name == tgt_nm and vertex.location == tgt_file:
                return vertex
        else:
            _process_node(vertex)

        if vertex not in visited:
            visited.append(vertex)
            stack.extend(vertex.children.values())


def _process_node(node: "Node"):
    print(node)


def get_obj_name(line: str) -> str:
    # TODO: implement regex for this in order to handle dunders
    clean_line = line.strip()

    if _line_blacklisted(line):
        return None

    no_def_found = not clean_line.startswith("def ")
    no_class_found = not clean_line.startswith("class ")

    if no_def_found and no_class_found:
        return None

    strip_chars = [":"]
    for replace_char in strip_chars:
        clean_line = clean_line.replace(replace_char, "")

    signature = clean_line.split()[1]
    name = signature.split("(")[0]
    
    return name


def get_node_type(line: str):
    obj_mappings = [
        ("def", FncNode), 
        ("class", ClsNode)
        ]
    obj_map = defaultdict(lambda: None, obj_mappings)

    clean_line = line.strip()
    first_word = clean_line.split()[0]

    return obj_map[first_word]


def get_next_nonempty_line(lines: list, place: int, length: int) -> str:
    # we're not applying the blacklisting rules here because both public
    # and private methods/functions should trigger the end of "this" obj

    place += 1

    while place <= length:
        line = lines[place]

        if not line.isspace():
            return line
            break

        place += 1

    return None
