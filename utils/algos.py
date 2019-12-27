from Node import Node


def xfs(node: Node, target: str, search_type: str = "dfs") -> Node:
    visited = []  # TODO: should implement __hash__ for Node so we can use a set
    stack = [node]

    if search_type == "bfs":
        from collections import deque
        stack = deque([node])

    while stack:
        vertex = stack.pop()

        if vertex.name == target:
            return vertex

        if vertex not in visited:
            visited.append(vertex)
            stack.extend(vertex.children.values())

    raise KeyError(f"node '{target}' not found in supplied graph")
