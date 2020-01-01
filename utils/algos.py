from Node import Node
from collections import deque


def xfs(node: Node, tgt_nm: str = None, tgt_file: str = None, search_type: str = "dfs") -> Node:
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


def process_node(node: Node):
    print(node)
