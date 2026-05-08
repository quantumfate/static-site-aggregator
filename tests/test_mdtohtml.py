import unittest

from markdown_convert import markdown_to_html_node


class TestMdToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>\n"
            "  <p>\n"
            "    This is \n"
            "    <b>bolded</b>\n"
            "     paragraph\n"
            "    text in a p\n"
            "    tag here\n"
            "  </p>\n"
            "  <p>\n"
            "    This is another paragraph with \n"
            "    <i>italic</i>\n"
            "     text and \n"
            "    <code>code</code>\n"
            "     here\n"
            "  </p>\n"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_simple_paragraph(self):
        md = "Hello world"
        html = markdown_to_html_node(md).to_html()
        expected = "<div>\n  <p>\n    Hello world\n  </p>\n</div>"
        self.assertEqual(html, expected)

    def test_empty_markdown(self):
        md = ""
        html = markdown_to_html_node(md).to_html()
        expected = "<div>\n</div>"
        self.assertEqual(html, expected)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>\n"
            "  <pre>\n"
            "    <code>\n"
            "      This is text that _should_ remain\n"
            "      the **same** even with inline stuff\n"
            "    </code>\n"
            "  </pre>\n"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_heading_h1(self):
        md = "# Big heading"
        html = markdown_to_html_node(md).to_html()
        expected = "<div>\n  <h1>\n    Big heading\n  </h1>\n</div>"
        self.assertEqual(html, expected)

    def test_heading_h6(self):
        md = "###### Six deep"
        html = markdown_to_html_node(md).to_html()
        expected = "<div>\n  <h6>\n    Six deep\n  </h6>\n</div>"
        self.assertEqual(html, expected)

    def test_blockquote(self):
        md = "> first line\n> second line"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div>\n"
            "  <blockquote>\n"
            "    first line\n"
            "    second line\n"
            "  </blockquote>\n"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_unordered_list(self):
        md = "- alpha\n- beta\n- gamma"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div>\n"
            "  <ul>\n"
            "    <li>alpha</li>\n"
            "    <li>beta</li>\n"
            "    <li>gamma</li>\n"
            "  </ul>\n"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = "1. one\n2. two\n3. three"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div>\n"
            "  <ol>\n"
            "    <li>one</li>\n"
            "    <li>two</li>\n"
            "    <li>three</li>\n"
            "  </ol>\n"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_link_inline(self):
        md = "Click [here](https://example.com) please"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div>\n"
            "  <p>\n"
            "    Click \n"
            '    <a href="https://example.com">here</a>\n'
            "     please\n"
            "  </p>\n"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_image_inline(self):
        md = "See ![alt text](img.png) yes"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div>\n"
            "  <p>\n"
            "    See \n"
            '    <img src="img.png" alt="alt text"></img>\n'
            "     yes\n"
            "  </p>\n"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_mixed_blocks(self):
        md = "# Title\n\nSome _para_.\n\n- a\n- b"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div>\n"
            "  <h1>\n"
            "    Title\n"
            "  </h1>\n"
            "  <p>\n"
            "    Some \n"
            "    <i>para</i>\n"
            "    .\n"
            "  </p>\n"
            "  <ul>\n"
            "    <li>a</li>\n"
            "    <li>b</li>\n"
            "  </ul>\n"
            "</div>"
        )
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
