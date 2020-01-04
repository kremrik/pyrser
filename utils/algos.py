from collections import deque


def xfs(node: "Node", tgt_nm: str = None, tgt_file: str = None, search_type: str = "dfs") -> "Node":
    # TODO: should implement __hash__ for Node so we can use a set
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
