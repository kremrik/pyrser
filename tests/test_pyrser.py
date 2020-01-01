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


if __name__ == "__main__":
    unittest.main(verbosity=2)
