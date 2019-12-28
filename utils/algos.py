from Node import Node


def xfs(node: Node, tgt_nm: str, tgt_typ: Node, search_type: str = "dfs") -> Node:
    # TODO: search by passing a Node instance or by passing name/type?
    # TODO: should implement __hash__ for Node so we can use a set
    visited = []  
    stack = [node]

    if search_type == "bfs":
        from collections import deque
        stack = deque([node])

    while stack:
        vertex = stack.pop()

        if vertex.name == tgt_nm and type(vertex) == tgt_typ:
            return vertex

        if vertex not in visited:
            visited.append(vertex)
            stack.extend(vertex.children.values())

    raise KeyError(f"node '{tgt_nm}' not found in supplied graph")
