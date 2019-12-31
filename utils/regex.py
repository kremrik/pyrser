import re


PATTERNS = {"function": re.compile(r"def ([a-z1-9_]*)"),
            "class": re.compile(r"class ([a-z1-9_]*)")}


def get_fnc_name(line: str):
    try:
        return PATTERNS["function"].findall(line)[0]
    except IndexError:
        return None
