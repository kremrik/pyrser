from utils.algos import xfs
from Node import PyNode, DirNode


if __name__ == "__main__":
    directory = DirNode("/path/to", "to")

    node = PyNode("/path/to/file.py", "file")
    node.name = "_module_"
    node.scope = [1, 12]

    fnc1 = PyNode("/path/to/file.py", "function1")
    fnc1.scope = [1, 2]

    fnc2 = PyNode("/path/to/file.py", "function2")
    fnc2.scope = [5, 6]

    fnc3 = PyNode("/path/to/file.py", "function3")
    fnc3.scope = [9, 11]

    fnc3_5 = PyNode("/path/to/file.py", "function3_5")
    fnc3_5.scope = [10, 11]

    fnc3.add_child(fnc3_5)
    node.add_child(fnc1)
    node.add_child(fnc2)
    node.add_child(fnc3)
    directory.add_child(node)

    res = xfs(directory, "function3_5")
    print(res)
    print(res.scope)
