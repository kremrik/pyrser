from pathlib import Path
import sys

pwd = str(Path(".").absolute())
sys.path.insert(0, pwd)

from Pyrser import pyrser
from Utils.PyrserHelpers import xfs
from Node import Node, DirNode, FileNode, ClsNode, FncNode
from ImportParser import get_fnc_calls, create_possible_import_path
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


class test_get_import_stmt(unittest.TestCase):

    def test_import_file(self):
        inpt_dir = "/home/kemri/Projects/pyrser/test_files/test_imports3/main.py"
        fnc_name = "fnc"
        gold = "from test import fnc"
        output = get_import_stmt(inpt_dir, fnc_name)
        self.assertEqual(gold, output)


class test_create_possible_import_path(unittest.TestCase):

    def test_import_file(self):
        import_stmt = "import file"
        cur_loc = "/path/to/main.py"
        gold = ("/path/to/file.py")
        
        output = create_possible_import_path(import_stmt, cur_loc)

        self.assertEqual(gold, output)

    def test_import_file(self):
        import_stmt = "import file1.file2"
        cur_loc = "/path/to/main.py"
        gold = ("/path/to/file.py")
        
        output = create_possible_import_path(import_stmt, cur_loc)

        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
