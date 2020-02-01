from Node import Node, FileNode
from Utils.PyrserHelpers import reader, xfs
import re
import os
from typing import Tuple, List


# https://stackoverflow.com/questions/9018947/regex-string-with-optional-parts
fnc_call_pattern = re.compile('(?P<location>[a-zA-Z0-9_.]+?\.)?(?P<call>[a-zA-Z0-9_]+?)\(')
import_pattern = re.compile(r"from ([a-zA-Z0-9_]*) import")


def get_fnc_calls(line: str) -> List[tuple]:
    if line.strip().startswith("def") or line.strip().startswith("class"):
        return ()

    output = fnc_call_pattern.findall(line)
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


def get_filepath_from_import(import_stmt: str, current_file: str) -> str:
    filename = import_pattern.findall(import_stmt)[0]
    parent_dir = get_parent_dir(current_file)
    sibling_files = get_sibling_files(parent_dir)
    host_file = get_host_file(sibling_files, filename)
    host_loc = os.path.join(parent_dir, host_file)
    
    return host_loc


def get_parent_dir(path: str) -> str:
    return os.path.dirname(path)


def get_sibling_files(path: str) -> List[str]:
    return [f for f in os.listdir(path) if f.endswith(".py")]


def get_host_file(sibling_files: List[str], name: str) -> str:
    return [f for f in sibling_files if name in f][0]


def get_node_from_func_call(fnc_call: tuple, current_file: str, graph: Node):
    file_alias, fnc_name = fnc_call

    if not file_alias:
        try_local = xfs(graph, fnc_name, current_file)
        
        if not try_local:
            import_stmt = get_import_stmt(current_file, fnc_name)
            import_path = get_filepath_from_import(import_stmt, current_file)
            return xfs(graph, fnc_name, import_path)
        else:
            return try_local

    else:
        parent_dir = get_parent_dir(current_file)
        sibling_files = get_sibling_files(parent_dir)
        host_file = get_host_file(sibling_files, file_alias)
        host_loc = os.path.join(parent_dir, host_file)
        return xfs(graph, fnc_name, host_loc)
