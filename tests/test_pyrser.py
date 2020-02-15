from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser, add_calls
from Node import DirNode, FileNode, ClsNode, FncNode
from Utils.PyrserHelpers import xfs
import unittest


def printer(*x):
    print("\n>>> OUTPUT <<<")
    print(*x, sep="\n")
    print()


@unittest.skip("skipping")
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

    def test_with_calls(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test6.py"

        filenode = FileNode(test_file, "test6.py")
        filenode.scope = [1, 6]

        fnc1 = FncNode(test_file, "say_hi")
        fnc1.scope = [1, 2]

        fnc2 = FncNode(test_file, "use_hi")
        fnc2.scope = [5, 6]
        fnc2.add_call(fnc1)

        filenode.add_child(fnc1)
        filenode.add_child(fnc2)
        gold = filenode

        output = pyrser(test_file)

        self.assertEqual(gold, output)

    def test_empty_dir(self):
        directory = "/home/kemri/Projects/pyrser/test_files/test_dir0"
        gold = DirNode(directory, "test_dir0")
        output = pyrser(directory)

        self.assertEqual(output, gold)

    def test_dir_with_no_py(self):
        directory = "/home/kemri/Projects/pyrser/test_files/test_dir1"
        gold = DirNode(directory, "test_dir1")
        output = pyrser(directory)

        self.assertEqual(output, gold)

    def test_dir_with_one_empty_py(self):
        directory = "/home/kemri/Projects/pyrser/test_files/test_dir2"
        gold = DirNode(directory, "test_dir2")
        output = pyrser(directory)

        self.assertEqual(output, gold)

    def test_dir_with_one_nonempty_py(self):
        directory = "/home/kemri/Projects/pyrser/test_files/test_dir3"

        dirnode = DirNode(directory, "test_dir3")

        filenode = FileNode(directory + "/test1.py", "test1.py")
        filenode.scope = [1, 3]

        fncnode = FncNode(directory + "/test1.py", "test")
        fncnode.parent = filenode
        fncnode.scope = [1, 3]

        filenode.add_child(fncnode)
        filenode.parent = dirnode
        
        dirnode.add_child(filenode)

        gold = dirnode
        output = pyrser(directory)

        self.assertEqual(output, gold)

    def test_dir_with_two_nonempty_py(self):
        directory = "/home/kemri/Projects/pyrser/test_files/test_dir4"

        dirnode = DirNode(directory, "test_dir4")

        filenode = FileNode(directory + "/test1.py", "test1.py")
        filenode.scope = [1, 3]
        fncnode = FncNode(directory + "/test1.py", "test")
        fncnode.parent = filenode
        fncnode.scope = [1, 3]
        filenode.add_child(fncnode)
        filenode.parent = dirnode
        dirnode.add_child(filenode)

        filenode2 = FileNode(directory + "/test2.py", "test2.py")
        filenode2.scope = [1, 3]
        fncnode2 = FncNode(directory + "/test2.py", "test")
        fncnode2.parent = filenode2
        fncnode2.scope = [1, 3]
        filenode2.add_child(fncnode2)
        filenode2.parent = dirnode
        dirnode.add_child(filenode2)

        gold = dirnode
        output = pyrser(directory)

        self.assertEqual(output, gold)

    def test_dir_within_dir(self):
        directory = "/home/kemri/Projects/pyrser/test_files/test_dir5"
        dirnode = DirNode(directory, "test_dir5")
        nested_dir = DirNode(directory + "/test_dir3", "test_dir3")
        nested_dir.parent = dirnode

        filenode = FileNode(directory + "/test_dir3" + "/test1.py", "test1.py")
        filenode.scope = [1, 3]
        fncnode = FncNode(directory + "/test_dir3" + "/test1.py", "test")
        fncnode.parent = filenode
        fncnode.scope = [1, 3]
        filenode.add_child(fncnode)
        filenode.parent = nested_dir
        nested_dir.add_child(filenode)
        dirnode.add_child(nested_dir)

        gold = dirnode
        output = pyrser(directory)

        self.assertEqual(output, gold)


class test_add_calls(unittest.TestCase):

    def test_simple_graph(self):
        input_graph = pyrser("/home/kemri/Projects/pyrser/test_files/test_imports4")

        gold_graph = pyrser("/home/kemri/Projects/pyrser/test_files/test_imports4")
        called_node = xfs(gold_graph, tgt_nm="fnc")
        caller_node = xfs(gold_graph, tgt_nm="main")
        caller_node.add_call(called_node)

        add_calls(input_graph)

        self.assertEqual(gold_graph, input_graph)


if __name__ == "__main__":
    unittest.main(verbosity=2)
