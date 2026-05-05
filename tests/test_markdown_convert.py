from markdown_convert import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType
import unittest


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_in_middle(self):
        result = split_nodes_delimiter(
            [
                TextNode(
                    "This is text with a **bolded phrase** in the middle", TextType.TEXT
                )
            ],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_italic_in_middle(self):
        result = split_nodes_delimiter(
            [TextNode("a _slanted_ word", TextType.TEXT)],
            "_",
            TextType.ITALIC,
        )
        self.assertEqual(
            result,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("slanted", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_code_in_middle(self):
        result = split_nodes_delimiter(
            [TextNode("run `ls -la` now", TextType.TEXT)],
            "`",
            TextType.CODE,
        )
        self.assertEqual(
            result,
            [
                TextNode("run ", TextType.TEXT),
                TextNode("ls -la", TextType.CODE),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start(self):
        result = split_nodes_delimiter(
            [TextNode("**bold** then plain", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            result,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" then plain", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        result = split_nodes_delimiter(
            [TextNode("plain then **bold**", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            result,
            [
                TextNode("plain then ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_whole_text_is_delimited(self):
        result = split_nodes_delimiter(
            [TextNode("**all bold**", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(result, [TextNode("all bold", TextType.BOLD)])

    def test_multiple_delimited_segments(self):
        result = split_nodes_delimiter(
            [TextNode("**one** and **two** and **three**", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            result,
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("three", TextType.BOLD),
            ],
        )

    def test_no_delimiter_in_text(self):
        result = split_nodes_delimiter(
            [TextNode("nothing special here", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(result, [TextNode("nothing special here", TextType.TEXT)])

    def test_unbalanced_delimiter_raises(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [TextNode("this **is broken", TextType.TEXT)],
                "**",
                TextType.BOLD,
            )

    def test_unbalanced_single_delimiter_raises(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [TextNode("dangling `code", TextType.TEXT)],
                "`",
                TextType.CODE,
            )

    def test_non_text_node_passes_through(self):
        already_bold = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([already_bold], "**", TextType.BOLD)
        self.assertEqual(result, [already_bold])

    def test_mixed_input_nodes(self):
        result = split_nodes_delimiter(
            [
                TextNode("plain with **bold** word", TextType.TEXT),
                TextNode("untouched", TextType.ITALIC),
                TextNode("more **bold** text", TextType.TEXT),
            ],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            result,
            [
                TextNode("plain with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
                TextNode("untouched", TextType.ITALIC),
                TextNode("more ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], "**", TextType.BOLD), [])

    def test_empty_text_node(self):
        result = split_nodes_delimiter(
            [TextNode("", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(result, [])

    def test_adjacent_delimited_segments(self):
        result = split_nodes_delimiter(
            [TextNode("**a****b**", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.BOLD),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_link_node_passes_through(self):
        link = TextNode("click", TextType.LINK, "https://example.com")
        result = split_nodes_delimiter([link], "**", TextType.BOLD)
        self.assertEqual(result, [link])


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        self.assertEqual(
            extract_markdown_images("![alt](https://example.com/img.png)"),
            [("alt", "https://example.com/img.png")],
        )

    def test_multiple_images(self):
        text = "![one](https://a.com/1.png) and ![two](https://b.com/2.jpg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("one", "https://a.com/1.png"), ("two", "https://b.com/2.jpg")],
        )

    def test_image_in_middle_of_text(self):
        self.assertEqual(
            extract_markdown_images("before ![alt](url) after"),
            [("alt", "url")],
        )

    def test_empty_alt(self):
        self.assertEqual(
            extract_markdown_images("![](https://example.com/x.png)"),
            [("", "https://example.com/x.png")],
        )

    def test_empty_url(self):
        self.assertEqual(extract_markdown_images("![alt]()"), [("alt", "")])

    def test_no_images(self):
        self.assertEqual(extract_markdown_images("plain text no images"), [])

    def test_link_not_matched_as_image(self):
        self.assertEqual(extract_markdown_images("[link](https://example.com)"), [])

    def test_mixed_image_and_link(self):
        text = "![img](https://a.com/i.png) and [link](https://b.com)"
        self.assertEqual(
            extract_markdown_images(text), [("img", "https://a.com/i.png")]
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        self.assertEqual(
            extract_markdown_links("[click](https://example.com)"),
            [("click", "https://example.com")],
        )

    def test_multiple_links(self):
        text = "[one](https://a.com) and [two](https://b.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("one", "https://a.com"), ("two", "https://b.com")],
        )

    def test_link_in_middle_of_text(self):
        self.assertEqual(
            extract_markdown_links("before [text](url) after"),
            [("text", "url")],
        )

    def test_empty_anchor(self):
        self.assertEqual(
            extract_markdown_links("[](https://example.com)"),
            [("", "https://example.com")],
        )

    def test_empty_url(self):
        self.assertEqual(extract_markdown_links("[anchor]()"), [("anchor", "")])

    def test_no_links(self):
        self.assertEqual(extract_markdown_links("plain text no links"), [])

    def test_image_not_matched_as_link(self):
        self.assertEqual(
            extract_markdown_links("![img](https://example.com/x.png)"), []
        )

    def test_mixed_image_and_link(self):
        text = "![img](https://a.com/i.png) and [link](https://b.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://b.com")])


if __name__ == "__main__":
    unittest.main()
