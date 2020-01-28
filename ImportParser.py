from Node import Node, FileNode
from Utils.PyrserHelpers import reader, xfs
import re
import os
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


def get_node_from_func_call(import_path: str, function: str, current_file: str, graph: Node):
    """
    A function that takes an import path like "module.file" and returns 
    a string denoting the path to the file it was imported from if it
    exists in the project, else it returns ""
    """
    if not import_path:
        return xfs(graph, function, current_file)

    parent_dir = os.path.dirname(current_file)
    import_file = parent_dir + "/" + import_path + ".py"
    
    return xfs(graph, function, import_file)
