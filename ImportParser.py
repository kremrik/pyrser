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


def get_import_stmt(filepath: str, fnc_name: str) -> str:
    with open(filepath, "r") as f:
        for line in f:
            if fnc_name in line and "import" in line:
                return line.strip()
        return ""


import_pattern = re.compile(r"from ([a-zA-Z0-9_]*) import")
def get_filepath_from_import(import_stmt: str, current_file: str) -> str:
    filename = import_pattern.findall(import_stmt)[0]
    parent_dir = os.path.dirname(current_file)
    sibling_files = [f for f in os.listdir(parent_dir) if f.endswith(".py")]
    host_file = [f for f in sibling_files if filename in f][0]
    host_loc = os.path.join(parent_dir, host_file)
    
    return host_loc


def get_node_from_func_call(fnc_call: tuple, current_file: str, graph: Node):
    file_alias, fnc_name = fnc_call

    if not file_alias:
        try_local = xfs(graph, fnc_name, current_file)
        
        if not try_local:
            import_stmt = get_import_stmt(current_file, fnc_name)
            import_path = get_filepath_from_import(import_stmt, current_file)
            return xfs(graph, fnc_name, import_path)
        
        return try_local

    else:
        parent_dir = os.path.dirname(current_file)
        sibling_files = [f for f in os.listdir(parent_dir) if f.endswith(".py")]
        host_file = [f for f in sibling_files if file_alias in f][0]
        host_loc = os.path.join(parent_dir, host_file)
        return xfs(graph, fnc_name, host_loc)
