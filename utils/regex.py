def get_obj_name(line: str):
    clean_line = line.strip()

    no_def_found = not clean_line.startswith("def ")
    no_class_found = not clean_line.startswith("class ")
    no_colon_found = not clean_line.endswith(":")

    if no_def_found and no_class_found and no_colon_found:
        return None

    strip_chars = ["(", ")", ":"]
    for replace_char in strip_chars:
        clean_line = clean_line.replace(replace_char, "")

    return clean_line.split()[1]
