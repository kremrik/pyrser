from Pyrser import pyrser, add_calls
from Utils.PyrserHelpers import reader, xfs, dfs_generator, get_file_name_from_path
from Node import Node, DirNode, FileNode, FncNode
import os


def nonempty_pyfile(path: str) -> bool:
    return path.endswith(".py") and os.path.getsize(path) > 0

def list_dir(path: str) -> bool:
    return os.listdir(path)

def is_dir(path: str) -> bool:
    return os.path.isdir(path)

def skip_file(path: str) -> bool:
    return not path.endswith(".py")

def make_dir_tree(path: str) -> Node:
    name = get_file_name_from_path(path)
    dirnode = DirNode(path, name)

    if nonempty_pyfile(path):
        return FileNode(path, name)

    for f in list_dir(path):
        next_file = os.path.join(path, f)
        print(next_file)
        dirnode.add_child(make_dir_tree(next_file))

    return dirnode

    
if __name__ == "__main__":
    test = "/home/kemri/Projects/pyrser/test_files"

    output = make_dir_tree(test)
    print(repr(output))
