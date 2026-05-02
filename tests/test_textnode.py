import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_text_type(self):
        node = TextNode(
            "This is a text node",
            "abritary",  # pyright: ignore[reportArgumentType]
        )
        self.assertNotIsInstance(node.text_type, TextType)

    def test_url_none(self):
        node = TextNode(
            "This is a text node",
            TextType.BOLD,
        )
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
