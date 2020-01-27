from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser
from Utils.PyrserHelpers import xfs
from Node import Node, DirNode, FileNode, ClsNode, FncNode
from ImportParser import get_fnc_calls, get_node_from_path
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


class test_get_node_from_path(unittest.TestCase):

    def test_function_in_current_file(self):
        test_file = "/path/to/test1.py"
        filenode = FileNode(test_file, "test1.py")
        fncnode = FncNode(test_file, "test")
        fncnode.parent = filenode
        filenode.add_child(fncnode)
        
        fnc_call = ("", "test")
        current_file = test_file
        graph = filenode

        gold = fncnode

        output = get_node_from_path(fnc_call, current_file, graph)

        self.assertEqual(gold, output)

    def test_no_function_in_current_file(self):
        test_file = "/path/to/test1.py"
        filenode = FileNode(test_file, "test1.py")
        fncnode = FncNode(test_file, "test")
        fncnode.parent = filenode
        filenode.add_child(fncnode)
        
        fnc_call = ("", "test_function")
        current_file = test_file
        graph = filenode

        gold = None

        output = get_node_from_path(fnc_call, current_file, graph)

        self.assertEqual(gold, output)

    def test_function_in_another_file(self):
        test_file = "/path/to/test1.py"
        filenode = FileNode(test_file, "test1.py")
        fncnode = FncNode(test_file, "test")
        fncnode.parent = filenode
        filenode.add_child(fncnode)
        
        fnc_call = ("test1", "test")
        current_file = "/path/to/another.py"
        graph = filenode

        gold = fncnode

        output = get_node_from_path(fnc_call, current_file, graph)

        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
