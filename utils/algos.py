from Node import Node
from collections import deque


def xfs(node: Node, tgt_nm: str, tgt_file: str, search_type: str = "dfs") -> Node:
    # TODO: should implement __hash__ for Node so we can use a set
    visited = []  
    stack = [node]

    if search_type == "bfs":
        stack = deque([node])

    while stack:
        vertex = stack.pop()

        if vertex.name == tgt_nm and vertex.location == tgt_file:
            return vertex

        if vertex not in visited:
            visited.append(vertex)
            stack.extend(vertex.children.values())

    raise KeyError(f"node '{tgt_nm}' not found in supplied graph")
