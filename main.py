from Pyrser import pyrser
from utils.algos import xfs, dfs_printer


if __name__ == "__main__":
    test_file = "/home/kemri/Projects/pyrser/test_files/test2.py"
    output = pyrser(test_file)
    print(repr(output))
    print(output.scope)
    print(list(output.children.values())[0].scope)
    print(list(output.children.values())[1].scope)
