from pathlib import Path
import sys

pwd = str(Path(".").absolute()); sys.path.insert(0, pwd)

from Utils.PyrserHelpers import get_obj_name
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
