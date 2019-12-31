from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser
from Node import DirNode, FileNode, ClsNode, FncNode
import unittest


def printer(*x):
    print("\n\n>>> OUTPUT <<<")
    print(*x, sep="\n")
    print()


class test_pyrser(unittest.TestCase):

    def test1(self):
        test_file = "/home/kemri/Projects/pyrser/test_files/test1.py"

        filenode = FileNode(test_file, "test1.py")
        filenode.scope = [1, 3]

        fncnode = FncNode(test_file, "test")
        fncnode.scope = [1, 3]

        filenode.add_child(fncnode)

        gold = filenode

        output = pyrser(test_file)

        printer(output, output.scope, output.children)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
