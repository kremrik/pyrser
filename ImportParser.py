from Node import Node, FileNode
from Utils.PyrserHelpers import xfs
import Utils.FileHelpers as fh
import re
from typing import Tuple, List


# https://stackoverflow.com/questions/9018947/regex-string-with-optional-parts
fnc_call_pattern = re.compile('(?P<location>[a-zA-Z0-9_.]+?\.)?(?P<call>[a-zA-Z0-9_]+?)\(')
from_file_import_function = re.compile(r"from ([a-zA-Z0-9_]*) import")
import_file = re.compile(r"import ([a-zA-Z0-9_]*)$")


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
    # TODO: refactor to use the reader in `fh`
    with open(filepath, "r") as f:
        for line in f:
            if fnc_name in line and "import" in line:
                return line.strip()
        return ""


def get_filepath_from_import(import_stmt: str, current_file: str) -> str:
    filename = from_file_import_function.findall(import_stmt) or import_file.findall(import_stmt)
    filename = filename[0]
    parent_dir = fh.get_parent_dir(current_file)
    sibling_files = fh.get_sibling_files(parent_dir)
    host_file = fh.get_host_file(sibling_files, filename)
    host_loc = fh.join_path(parent_dir, host_file)
    
    return host_loc


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
        parent_dir = fh.get_parent_dir(current_file)
        sibling_files = fh.get_sibling_files(parent_dir)
        host_file = fh.get_host_file(sibling_files, file_alias)
        host_loc = fh.join_path(parent_dir, host_file)
        return xfs(graph, fnc_name, host_loc)
