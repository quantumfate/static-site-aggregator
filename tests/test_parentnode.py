from leafnode import LeafNode
from parentnode import ParentNode
import unittest


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag_raise(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode(
            None,  # pyright: ignore[reportArgumentType]
            [child_node],
        )
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_no_child_rais(self):
        parent_node = ParentNode(
            "div",
            None,
        )
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_nested(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "Paragraph"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><b>Bold text</b>Normal text<div><p>Paragraph</p>Normal text<i>italic text</i>Normal text</div>Normal text</div>",
        )


if __name__ == "__main__":
    unittest.main()
