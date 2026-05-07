from markdown_convert import (
    markdown_to_blocks,
    split_nodes_delimiter,
    match_links,
    match_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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


def _pairs(matches):
    return [(m.group(1), m.group(2)) for m in matches]


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        self.assertEqual(
            _pairs(match_images("![alt](https://example.com/img.png)")),
            [("alt", "https://example.com/img.png")],
        )

    def test_multiple_images(self):
        text = "![one](https://a.com/1.png) and ![two](https://b.com/2.jpg)"
        self.assertEqual(
            _pairs(match_images(text)),
            [("one", "https://a.com/1.png"), ("two", "https://b.com/2.jpg")],
        )

    def test_image_in_middle_of_text(self):
        self.assertEqual(
            _pairs(match_images("before ![alt](url) after")),
            [("alt", "url")],
        )

    def test_empty_alt(self):
        self.assertEqual(
            _pairs(match_images("![](https://example.com/x.png)")),
            [("", "https://example.com/x.png")],
        )

    def test_empty_url(self):
        self.assertEqual(_pairs(match_images("![alt]()")), [("alt", "")])

    def test_no_images(self):
        self.assertEqual(_pairs(match_images("plain text no images")), [])

    def test_link_not_matched_as_image(self):
        self.assertEqual(_pairs(match_images("[link](https://example.com)")), [])

    def test_mixed_image_and_link(self):
        text = "![img](https://a.com/i.png) and [link](https://b.com)"
        self.assertEqual(_pairs(match_images(text)), [("img", "https://a.com/i.png")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        self.assertEqual(
            _pairs(match_links("[click](https://example.com)")),
            [("click", "https://example.com")],
        )

    def test_multiple_links(self):
        text = "[one](https://a.com) and [two](https://b.com)"
        self.assertEqual(
            _pairs(match_links(text)),
            [("one", "https://a.com"), ("two", "https://b.com")],
        )

    def test_link_in_middle_of_text(self):
        self.assertEqual(
            _pairs(match_links("before [text](url) after")),
            [("text", "url")],
        )

    def test_empty_anchor(self):
        self.assertEqual(
            _pairs(match_links("[](https://example.com)")),
            [("", "https://example.com")],
        )

    def test_empty_url(self):
        self.assertEqual(_pairs(match_links("[anchor]()")), [("anchor", "")])

    def test_no_links(self):
        self.assertEqual(_pairs(match_links("plain text no links")), [])

    def test_image_not_matched_as_link(self):
        self.assertEqual(_pairs(match_links("![img](https://example.com/x.png)")), [])

    def test_mixed_image_and_link(self):
        text = "![img](https://a.com/i.png) and [link](https://b.com)"
        self.assertEqual(_pairs(match_links(text)), [("link", "https://b.com")])


class TestSplitNodesMedia(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        result = split_nodes_image(
            [TextNode("![alt](https://a.com/x.png)", TextType.TEXT)]
        )
        self.assertEqual(
            result,
            [TextNode("alt", TextType.IMAGE, "https://a.com/x.png")],
        )

    def test_image_at_start(self):
        result = split_nodes_image(
            [TextNode("![alt](https://a.com/x.png) trailing", TextType.TEXT)]
        )
        self.assertEqual(
            result,
            [
                TextNode("alt", TextType.IMAGE, "https://a.com/x.png"),
                TextNode(" trailing", TextType.TEXT),
            ],
        )

    def test_image_at_end(self):
        result = split_nodes_image(
            [TextNode("leading ![alt](https://a.com/x.png)", TextType.TEXT)]
        )
        self.assertEqual(
            result,
            [
                TextNode("leading ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://a.com/x.png"),
            ],
        )

    def test_text_after_last_image_preserved(self):
        result = split_nodes_image(
            [TextNode("pre ![a](u1) mid ![b](u2) tail", TextType.TEXT)]
        )
        self.assertEqual(
            result,
            [
                TextNode("pre ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "u1"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "u2"),
                TextNode(" tail", TextType.TEXT),
            ],
        )

    def test_adjacent_images(self):
        result = split_nodes_image([TextNode("![a](u1)![b](u2)", TextType.TEXT)])
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.IMAGE, "u1"),
                TextNode("b", TextType.IMAGE, "u2"),
            ],
        )

    def test_no_images_passes_through(self):
        node = TextNode("plain text with [link](https://a.com)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_non_text_node_passes_through(self):
        bold = TextNode("bold", TextType.BOLD)
        self.assertEqual(split_nodes_image([bold]), [bold])

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_mixed_input_nodes(self):
        result = split_nodes_image(
            [
                TextNode("first ![a](u1) end", TextType.TEXT),
                TextNode("untouched", TextType.BOLD),
                TextNode("![b](u2) only", TextType.TEXT),
            ]
        )
        self.assertEqual(
            result,
            [
                TextNode("first ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "u1"),
                TextNode(" end", TextType.TEXT),
                TextNode("untouched", TextType.BOLD),
                TextNode("b", TextType.IMAGE, "u2"),
                TextNode(" only", TextType.TEXT),
            ],
        )

    def test_link_in_text_not_split_as_image(self):
        node = TextNode("see [link](https://a.com) here", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        result = split_nodes_link([TextNode("[click](https://a.com)", TextType.TEXT)])
        self.assertEqual(
            result,
            [TextNode("click", TextType.LINK, "https://a.com")],
        )

    def test_link_at_start(self):
        result = split_nodes_link(
            [TextNode("[click](https://a.com) trailing", TextType.TEXT)]
        )
        self.assertEqual(
            result,
            [
                TextNode("click", TextType.LINK, "https://a.com"),
                TextNode(" trailing", TextType.TEXT),
            ],
        )

    def test_link_at_end(self):
        result = split_nodes_link(
            [TextNode("leading [click](https://a.com)", TextType.TEXT)]
        )
        self.assertEqual(
            result,
            [
                TextNode("leading ", TextType.TEXT),
                TextNode("click", TextType.LINK, "https://a.com"),
            ],
        )

    def test_multiple_links_with_trailing_text(self):
        result = split_nodes_link(
            [TextNode("pre [a](u1) mid [b](u2) tail", TextType.TEXT)]
        )
        self.assertEqual(
            result,
            [
                TextNode("pre ", TextType.TEXT),
                TextNode("a", TextType.LINK, "u1"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("b", TextType.LINK, "u2"),
                TextNode(" tail", TextType.TEXT),
            ],
        )

    def test_adjacent_links(self):
        result = split_nodes_link([TextNode("[a](u1)[b](u2)", TextType.TEXT)])
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.LINK, "u1"),
                TextNode("b", TextType.LINK, "u2"),
            ],
        )

    def test_no_links_passes_through(self):
        node = TextNode("plain text no links", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_non_text_node_passes_through(self):
        italic = TextNode("italic", TextType.ITALIC)
        self.assertEqual(split_nodes_link([italic]), [italic])

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_link([]), [])

    def test_image_in_text_not_split_as_link(self):
        node = TextNode("see ![img](https://a.com/x.png) here", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_mixed_image_and_link_only_links_split(self):
        result = split_nodes_link(
            [
                TextNode(
                    "![img](https://a.com/x.png) and [link](https://b.com)",
                    TextType.TEXT,
                )
            ]
        )
        self.assertEqual(
            result,
            [
                TextNode("![img](https://a.com/x.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://b.com"),
            ],
        )

    def test_mixed_input_nodes(self):
        result = split_nodes_link(
            [
                TextNode("first [a](u1) end", TextType.TEXT),
                TextNode("untouched", TextType.BOLD),
                TextNode("[b](u2) only", TextType.TEXT),
            ]
        )
        self.assertEqual(
            result,
            [
                TextNode("first ", TextType.TEXT),
                TextNode("a", TextType.LINK, "u1"),
                TextNode(" end", TextType.TEXT),
                TextNode("untouched", TextType.BOLD),
                TextNode("b", TextType.LINK, "u2"),
                TextNode(" only", TextType.TEXT),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test(self):
        self.assertEqual(
            text_to_textnodes(
                "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            ),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_plain_text(self):
        self.assertEqual(
            text_to_textnodes("just some plain text"),
            [TextNode("just some plain text", TextType.TEXT)],
        )

    def test_empty_string(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_only_bold(self):
        self.assertEqual(
            text_to_textnodes("**all bold**"),
            [TextNode("all bold", TextType.BOLD)],
        )

    def test_only_italic(self):
        self.assertEqual(
            text_to_textnodes("_all italic_"),
            [TextNode("all italic", TextType.ITALIC)],
        )

    def test_only_code(self):
        self.assertEqual(
            text_to_textnodes("`all code`"),
            [TextNode("all code", TextType.CODE)],
        )

    def test_only_image(self):
        self.assertEqual(
            text_to_textnodes("![alt](https://a.com/x.png)"),
            [TextNode("alt", TextType.IMAGE, "https://a.com/x.png")],
        )

    def test_only_link(self):
        self.assertEqual(
            text_to_textnodes("[click](https://a.com)"),
            [TextNode("click", TextType.LINK, "https://a.com")],
        )

    def test_adjacent_inline_styles(self):
        self.assertEqual(
            text_to_textnodes("**bold**_italic_`code`"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_multiple_same_type(self):
        self.assertEqual(
            text_to_textnodes("**a** and **b** and **c**"),
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("c", TextType.BOLD),
            ],
        )

    def test_image_and_link_mixed(self):
        self.assertEqual(
            text_to_textnodes(
                "see ![pic](https://a.com/x.png) then [go](https://b.com)"
            ),
            [
                TextNode("see ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://a.com/x.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("go", TextType.LINK, "https://b.com"),
            ],
        )

    def test_link_before_image(self):
        self.assertEqual(
            text_to_textnodes("[a](u1) and ![b](u2)"),
            [
                TextNode("a", TextType.LINK, "u1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "u2"),
            ],
        )

    def test_styles_around_media(self):
        self.assertEqual(
            text_to_textnodes("**bold** then [link](https://a.com) end"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" then ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_unbalanced_bold_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("this **is broken")

    def test_unbalanced_code_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("dangling `code")

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_block(self):
        self.assertEqual(
            markdown_to_blocks("just one paragraph"),
            ["just one paragraph"],
        )

    def test_two_simple_blocks(self):
        self.assertEqual(
            markdown_to_blocks("first block\n\nsecond block"),
            ["first block", "second block"],
        )

    def test_strips_leading_and_trailing_whitespace(self):
        self.assertEqual(
            markdown_to_blocks("   leading and trailing   \n\n   block two   "),
            ["leading and trailing", "block two"],
        )

    def test_excessive_blank_lines_between_blocks(self):
        self.assertEqual(
            markdown_to_blocks("a\n\n\n\nb"),
            ["a", "b"],
        )

    def test_leading_and_trailing_blank_lines(self):
        self.assertEqual(
            markdown_to_blocks("\n\nonly block\n\n"),
            ["only block"],
        )

    def test_preserves_internal_single_newlines(self):
        self.assertEqual(
            markdown_to_blocks("line one\nline two\n\nnext block"),
            ["line one\nline two", "next block"],
        )

    def test_heading_and_paragraph(self):
        self.assertEqual(
            markdown_to_blocks("# Heading\n\nParagraph text"),
            ["# Heading", "Paragraph text"],
        )

    def test_unordered_list_block(self):
        self.assertEqual(
            markdown_to_blocks("- item 1\n- item 2\n- item 3"),
            ["- item 1\n- item 2\n- item 3"],
        )

    def test_ordered_list_block(self):
        self.assertEqual(
            markdown_to_blocks("1. first\n2. second\n3. third"),
            ["1. first\n2. second\n3. third"],
        )

    def test_quote_block(self):
        self.assertEqual(
            markdown_to_blocks("> quoted line one\n> quoted line two"),
            ["> quoted line one\n> quoted line two"],
        )

    def test_mixed_block_types(self):
        md = "# Title\n\nParagraph with **bold**.\n\n- a\n- b\n\n> quote"
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Title",
                "Paragraph with **bold**.",
                "- a\n- b",
                "> quote",
            ],
        )

    def test_only_newlines(self):
        self.assertEqual(markdown_to_blocks("\n\n\n\n"), [])

    def test_block_with_inline_markdown_preserved(self):
        self.assertEqual(
            markdown_to_blocks(
                "This has **bold** and _italic_ and `code`\n\n![img](u) and [link](u2)"
            ),
            [
                "This has **bold** and _italic_ and `code`",
                "![img](u) and [link](u2)",
            ],
        )

    def test_returns_list_type(self):
        self.assertIsInstance(markdown_to_blocks("a\n\nb"), list)


if __name__ == "__main__":
    unittest.main()
