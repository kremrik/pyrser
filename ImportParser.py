from Node import Node, FileNode
from Utils.PyrserHelpers import reader, xfs
import re
from typing import Tuple


pattern = re.compile('(?P<location>[a-zA-Z0-9_]+?\.)?(?P<call>[a-zA-Z0-9_]+?)\(')


def get_fnc_calls(line: str):
    if line.strip().startswith("def") or line.strip().startswith("class"):
        return ()

    return pattern.findall(line)


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
