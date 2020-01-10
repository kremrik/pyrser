from Pyrser import pyrser
from Utils.PyrserHelpers import get_next_nonempty_line
from Node import FileNode, FncNode


if __name__ == "__main__":
    test_file = "/home/kemri/Projects/pyrser/Node.py"
    output = pyrser(test_file)
    print(repr(output))

    # test1 = FileNode("/path/to/test1.py", "test1.py")
    # test2 = FncNode("/path/to/test1.py", "test")
    # test1.add_child(test2)
    # test2.parent = test1
    # print(test2)
