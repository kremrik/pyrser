from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser
from Utils.PyrserHelpers import xfs
from Node import Node, DirNode, FileNode, ClsNode, FncNode
from ImportParser import get_fnc_calls, get_node_from_func_call
import unittest


class test_get_fnc_calls(unittest.TestCase):

    def test_empty_call_without_alias(self):
        inpt = "test_call()"
        gold = [("", "test_call")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)

    def test_args_call_without_alias(self):
        inpt = "test_call(arg)"
        gold = [("", "test_call")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)

    def test_call_with_alias(self):
        inpt = "module.test_call()"
        gold = [("module", "test_call")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)

    def test_call_with_multiple_aliases(self):
        inpt = "module.file.test_call()"
        gold = [("module.file", "test_call")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)

    def test_call_with_multiple_aliases_and_arg(self):
        inpt = "module.file.test_call(test)"
        gold = [("module.file", "test_call")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)

    def test_nested_calls(self):
        inpt = "module1.file1.fnc1(module2.file2.fnc2(arg1, arg2))"
        gold = [("module1.file1", "fnc1"), ("module2.file2", "fnc2")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)

    def test_multiple_calls_sep_by_semicolon(self):
        inpt = "module1.file1.fnc1(); module2.file2.fnc2(arg1, arg2))"
        gold = [("module1.file1", "fnc1"), ("module2.file2", "fnc2")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)

    def test_multiple_calls_no_aliases(self):
        inpt = "fnc1(); fnc2(arg1, arg2))"
        gold = [("", "fnc1"), ("", "fnc2")]
        output = get_fnc_calls(inpt)
        self.assertEqual(gold, output)


class test_get_node_from_func_call(unittest.TestCase):
    """takes input from get_fnc_calls"""

    def test_fnc_defined_in_this_file(self):
        inpt = ("", "fnc")
        inpt_dir = "/home/kemri/Projects/pyrser/test_files/test_imports1"
        curr_file = inpt_dir + "/file.py"
        graph = pyrser(inpt_dir)
        gold = FncNode(inpt_dir + "/file.py", "fnc"); gold.scope = [1, 2]
        output = get_node_from_func_call(inpt, curr_file, graph)
        self.assertEqual(gold, output)

    def test_fnc_imported_from_sibling_file(self):
        inpt = ("test", "fnc")
        inpt_dir = "/home/kemri/Projects/pyrser/test_files/test_imports2"
        curr_file = inpt_dir + "/main.py"
        graph = pyrser(inpt_dir)
        gold = FncNode(inpt_dir + "/test.py", "fnc"); gold.scope = [1, 2]
        output = get_node_from_func_call(inpt, curr_file, graph)
        self.assertEqual(gold, output)
        

if __name__ == "__main__":
    unittest.main(verbosity=2)
