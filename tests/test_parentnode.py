from leafnode import LeafNode
from parentnode import ParentNode
import unittest


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div>\n  <span>child</span>\n</div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div>\n  <span>\n    <b>grandchild</b>\n  </span>\n</div>",
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
            "<div>\n  <b>Bold text</b>\n  Normal text\n  <div>\n    <p>Paragraph</p>\n    Normal text\n    <i>italic text</i>\n    Normal text\n  </div>\n  Normal text\n</div>",
        )


if __name__ == "__main__":
    unittest.main()
