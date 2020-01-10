from Node import DirNode, FileNode, ClsNode, FncNode
from collections import deque, defaultdict
import ntpath


IGNORE_LEADING_CHARS = ["__"]


def reader(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines =f.readlines()
    return lines


def is_file(path: str) -> bool:
    return ntpath.isfile(path)


def get_file_name_from_path(path: str) -> str:
    return ntpath.basename(path)


def xfs(node: "Node", tgt_nm: str = None, tgt_file: str = None, search_type: str = "dfs") -> "Node":
    # TODO: could implement __hash__ for Node so we can use a set
    visited = []  
    stack = deque([node]) if search_type == "bfs" else [node]

    while stack:
        vertex = stack.pop()

        if tgt_nm and tgt_file:
            if vertex.name == tgt_nm and vertex.location == tgt_file:
                return vertex
        else:
            process_node(vertex)

        if vertex not in visited:
            visited.append(vertex)
            stack.extend(vertex.children.values())


def process_node(node: "Node"):
    print(node)


def get_obj_name(line: str) -> str:
    clean_line = line.strip()

    no_def_found = not clean_line.startswith("def ")
    no_class_found = not clean_line.startswith("class ")
    not_blacklisted = not is_line_blacklisted(line)

    if no_def_found and no_class_found:
        return None

    strip_chars = [":"]
    for replace_char in strip_chars:
        clean_line = clean_line.replace(replace_char, "")

    signature = clean_line.split()[1]
    name = signature.split("(")[0]
    
    return name


def is_line_blacklisted(line: str) -> bool:
    for chars in IGNORE_LEADING_CHARS:
        if chars in line:
            return True
    return False


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
    place += 1

    while place <= length:
        line = lines[place]

        if not line.isspace():
            return line
            break

        place += 1

    return None
