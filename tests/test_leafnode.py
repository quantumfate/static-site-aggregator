from leafnode import LeafNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_raise_error(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
