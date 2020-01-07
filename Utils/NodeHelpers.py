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
