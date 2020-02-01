"""
TODO: create more sophisticated blacklisting function to handle things like `.git`
"""


BLACKLIST_CHARS = ["__"]


def line_blacklisted(line: str) -> bool:
    # TODO: convert to decorator

    for chars in BLACKLIST_CHARS:
        if chars in line:
            return True
    return False
