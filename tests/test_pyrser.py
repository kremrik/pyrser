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
        fncnode = FncNode("/home/kemri/Projects/pyrser/test_files/test1.py", "test")
        fncnode.scope = [1, 3]
        gold = fncnode

        test_file = "/home/kemri/Projects/pyrser/test_files/test1.py"
        output = pyrser(test_file)

        printer(output, output.scope)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
