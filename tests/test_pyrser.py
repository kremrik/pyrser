from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser
from Node import DirNode, FileNode, ClsNode, FncNode
import unittest


def printer(*x):
    print("\n>>> OUTPUT <<<")
    print(*x, sep="\n")
    print()


class test_pyrser(unittest.TestCase):

    def test_empty_file(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test0.py"
        
        filenode = FileNode(test_file, "test0.py")
        filenode.scope = [1, 1]
        gold = filenode

        output = pyrser(test_file)
        
        self.assertEqual(gold, output)

    def test_one_function(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test1.py"

        filenode = FileNode(test_file, "test1.py")
        filenode.scope = [1, 3]
        fncnode = FncNode(test_file, "test")
        fncnode.scope = [1, 3]
        fncnode.parent = filenode
        filenode.add_child(fncnode)
        gold = filenode

        output = pyrser(test_file)

        self.assertEqual(gold, output)

    def test_two_functions(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test2.py"

        filenode = FileNode(test_file, "test2.py")
        filenode.scope = [1, 6]

        test = FncNode(test_file, "test")
        test.scope = [1, 3]
        test.parent = filenode

        test2 = FncNode(test_file, "test2")
        test2.scope = [5, 6]
        test2.parent = filenode

        filenode.add_child(test)
        filenode.add_child(test2)
        gold = filenode

        output = pyrser(test_file)
        
        self.assertEqual(gold, output)

    def test_nested_function_at_end(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test3.py"

        filenode = FileNode(test_file, "test3.py")
        filenode.scope = [1, 7]

        test = FncNode(test_file, "test")
        test.scope = [1, 3]
        test.parent = filenode

        test2 = FncNode(test_file, "test2")
        test2.scope = [5, 7]
        test2.parent = filenode

        test2_1 = FncNode(test_file, "test2_1")
        test2_1.scope = [6, 7]
        test2_1.parent = test2

        filenode.add_child(test)
        test2.add_child(test2_1)
        filenode.add_child(test2)
        gold = filenode

        output = pyrser(test_file)
        
        self.assertEqual(gold, output)

    def test_nested_function_with_simple_after(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test4.py"

        filenode = FileNode(test_file, "test4.py")
        filenode.scope = [1, 6]

        test1 = FncNode(test_file, "test1")
        test1.scope = [1, 3]
        test1.parent = filenode

        test1_1 = FncNode(test_file, "test1_1")
        test1_1.scope = [2, 3]
        test1_1.parent = test1

        test2 = FncNode(test_file, "test2")
        test2.scope = [5, 6]
        test2.parent = filenode

        filenode.add_child(test1)
        test1.add_child(test1_1)
        filenode.add_child(test2)
        gold = filenode

        output = pyrser(test_file)

        self.assertEqual(gold, output)

    def test_mixed_classes_and_functions(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test5.py"

        filenode = FileNode(test_file, "test5.py")
        filenode.scope = [1, 16]

        fnc1 = FncNode(test_file, "fnc1")
        fnc1.scope = [1, 3]
        inner = FncNode(test_file, "inner")
        inner.scope = [2, 3]
        fnc1.add_child(inner)

        cls1 = ClsNode(test_file, "cls1")
        cls1.scope = [6, 8]
        init = FncNode(test_file, "__init__")
        init.scope = [7, 8]
        cls1.add_child(init)

        cls2 = ClsNode(test_file, "cls2")
        cls2.scope = [11, 12]

        fnc2 = FncNode(test_file, "fnc2")
        fnc2.scope = [15, 16]

        filenode.add_child(fnc1)
        filenode.add_child(cls1)
        filenode.add_child(cls2)
        filenode.add_child(fnc2)
        gold = filenode

        output = pyrser(test_file)

        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
