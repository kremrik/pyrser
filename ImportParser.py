from Node import Node, FileNode
from Utils.PyrserHelpers import xfs
import Utils.FileHelpers as fh
import re
from typing import Tuple, List
from functools import lru_cache


# https://stackoverflow.com/questions/9018947/regex-string-with-optional-parts
fnc_call_pattern = re.compile('(?P<location>[a-zA-Z0-9_.]+?\.)?(?P<call>[a-zA-Z0-9_]+?)\(')
from_file_import_function = re.compile(r"from ([a-zA-Z0-9_.]*) import")
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


@lru_cache(maxsize=None)
def get_import_stmt(filepath: str, fnc_name: str) -> str:
    # TODO: refactor to use the reader in `fh`
    with open(filepath, "r") as f:
        for line in f:
            if fnc_name in line and "import" in line:
                return line.strip()
        return ""
