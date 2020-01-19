from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser
from Utils.PyrserHelpers import xfs
from Node import Node, DirNode, FileNode, ClsNode, FncNode
from ImportParser import add_calls
import unittest


class test_ImportParser(unittest.TestCase):

    def test_from_module_import_file(self):
        path = "/home/kemri/Projects/pyrser/test_files/test_imports1"
        path_file = path + "/file1.py"

        called_gold = FncNode(location=path_file, name="fnc")
        called_gold.scope = [1, 2]

        graph = pyrser(path)
        graph_with_calls = add_calls(graph)

        # self.assertEqual(xfs(graph_with_calls, "fnc", path_file), called_gold)


if __name__ == "__main__":
    unittest.main(verbosity=2)
