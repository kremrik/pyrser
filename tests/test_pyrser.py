from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser
from Node import DirNode, FileNode, ClsNode, FncNode
from utils.algos import xfs
import unittest


def printer(*x):
    print("\n>>> OUTPUT <<<")
    print(*x, sep="\n")
    print()


class test_pyrser(unittest.TestCase):

    def test0(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test0.py"
        
        filenode = FileNode(test_file, "test0.py")
        filenode.scope = [1, 1]
        gold = filenode

        output = pyrser(test_file)
        
        self.assertEqual(gold, output)

    def test1(self):
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

    def test2(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test2.py"

        filenode = FileNode(test_file, "test2.py")
        filenode.scope = [1, 5]

        test = FncNode(test_file, "test")
        test.scope = [1, 3]
        test.parent = filenode

        test2 = FncNode(test_file, "test2")
        test2.scope = [4, 5]
        test2.parent = filenode

        filenode.add_child(test)
        filenode.add_child(test2)
        gold = filenode

        output = pyrser(test_file)
        
        self.assertEqual(gold, output)

    @unittest.skip("working on 1 and 2")
    def test3(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test3.py"

        filenode = FileNode(test_file, "test3.py")
        filenode.scope = [1, 6]

        test = FncNode(test_file, "test")
        test.scope = [1, 3]
        test.parent = filenode

        test2 = FncNode(test_file, "test2")
        test2.scope = [4, 6]
        test2.parent = filenode

        test2_1 = FncNode(test_file, "test2_1")
        test2_1.scope = [5, 6]
        test2_1.parent = test2

        filenode.add_child(test)
        test2.add_child(test2_1)
        filenode.add_child(test2)
        gold = filenode

        output = pyrser(test_file)
        print()
        xfs(output)
        
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
