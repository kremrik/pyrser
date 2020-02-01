from pathlib import Path
import sys

pwd = str(Path(".").absolute()); sys.path.insert(0, pwd)

from Node import DirNode, FileNode
from Utils.PyrserHelpers import get_obj_name, get_fnc_calls, get_fnc_from_line
import unittest


class test_get_obj_name(unittest.TestCase):

    def test_simple_fnc(self):
        output = get_obj_name("def test():")
        gold = "test"
        self.assertEqual(output, gold)

    def test_simple_class(self):
        output = get_obj_name("class test(object):")
        gold = "test"
        self.assertEqual(output, gold)

    def test_whitespace_fnc(self):
        output = get_obj_name("    def test():")
        gold = "test"
        self.assertEqual(output, gold)

    def test_whitespace_cls(self):
        output = get_obj_name("    class test(object):")
        gold = "test"
        self.assertEqual(output, gold)

    def test_fnc_with_arg(self):
        output = get_obj_name("def test(arg):")
        gold = "test"
        self.assertEqual(output, gold)

    def test_cls_without_arg(self):
        output = get_obj_name("class test:")
        gold = "test"
        self.assertEqual(output, gold)


class test_get_fnc_calls(unittest.TestCase):
    
    def test_fnc_no_params(self):
        output = get_fnc_calls("test()")
        self.assertEqual(output, ("test",))

    def test_fnc_with_params(self):
        output = get_fnc_calls("test(x)")
        self.assertEqual(output, ("test",))

    def test_multiple_fncs(self):
        output = get_fnc_calls("test(); test2()")
        self.assertEqual(output, ("test", "test2"))

    def test_aliased_fnc(self):
        output = get_fnc_calls("a.test()")
        self.assertEqual(output, ("test",))

    def test_returns_falsy(self):
        output = get_fnc_calls("a = 'hi'")
        self.assertEqual(output, ())

    def test_doesnt_catch_def(self):
        output = get_fnc_calls("def test():")
        self.assertEqual(output, ())

    
class test_get_fnc_from_line(unittest.TestCase):

    def test_simple(self):
        lines = ['def use_hi():\n',
                 '    say_hi()\n']
        place = 1
        output = get_fnc_from_line(lines, place)
        self.assertEqual(output, "use_hi")

    def test_private(self):
        lines = ['def __init__(self):\n',
                 '    say_hi()\n']
        place = 1
        output = get_fnc_from_line(lines, place)
        self.assertEqual(output, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
