from Node import Node, FileNode
from Utils.PyrserHelpers import reader, xfs
import re
from typing import Tuple, List


# https://stackoverflow.com/questions/9018947/regex-string-with-optional-parts
pattern = re.compile('(?P<location>[a-zA-Z0-9_.]+?\.)?(?P<call>[a-zA-Z0-9_]+?)\(')


def get_fnc_calls(line: str) -> List[tuple]:
    if line.strip().startswith("def") or line.strip().startswith("class"):
        return ()

    output = pattern.findall(line)
    cleaned_output = [
        (x[:-1], y) 
        if x.endswith(".") 
        else (x, y) 
        for x, y in output]

    return cleaned_output


def get_node_from_path(fnc_call: tuple, current_file: str, graph: Node):
    if fnc_call[0]:
        pass
    else:
        return xfs(graph, fnc_call[1], current_file)


def add_calls(graph: Node) -> Node:
    """
    `graph` is a fully populated ``Node`` object, which means it contains all the 
    paths necessary to fully traverse the package, module, or file. And it does
    not matter how we traverse it either, only that we hit every vertex.
    """

    for node in graph:
        if type(node) == FileNode:
            lines = reader(node.location)
            

    print(repr(graph))
