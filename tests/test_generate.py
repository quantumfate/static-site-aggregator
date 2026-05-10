import unittest
from generate import extract_title


class TestGenerate(unittest.TestCase):
    def test_simple_h1(self):
        extracted = extract_title("# This is a title")
        self.assertEqual(extracted, "This is a title")

    def test_is_h1(self):
        self.assertRaises(ValueError, extract_title, "## This is a title")

    def test_simple_raise(self):
        self.assertRaises(ValueError, extract_title, "#This is a title")
