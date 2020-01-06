from collections import deque
import ntpath


def reader(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines = [line for line in f.readlines() if line != "\n"]
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


def format_branch(node: "Node", level: int) -> str:
    left_pad = " " * 1 if level > 0 else ""
    parent_bars = "|    " * (level - 1)
    branch_bar = "|-- " if level > 0 else ""
    show = left_pad + parent_bars + branch_bar + str(node) + "\n"

    return show


def dfs_printer(node: "Node", level: int = 0, visited: list = None) -> None:
    output = ""

    if visited is None:
        visited = []
    
    show = format_branch(node, level)
    output = output + show

    visited.append(node)

    for child in node.children.values():
        output = output + dfs_printer(child, level+1, visited)

    return output


def get_obj_name(line: str):
    clean_line = line.strip()

    no_def_found = not clean_line.startswith("def ")
    no_class_found = not clean_line.startswith("class ")
    no_colon_found = not clean_line.endswith(":")

    if no_def_found and no_class_found and no_colon_found:
        return None

    strip_chars = [":"]
    for replace_char in strip_chars:
        clean_line = clean_line.replace(replace_char, "")

    signature = clean_line.split()[1]
    name = signature.split("(")[0]
    
    return name
