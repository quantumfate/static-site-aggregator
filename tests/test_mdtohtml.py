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
            "<div>"
            "<p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_simple_paragraph(self):
        md = "Hello world"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><p>Hello world</p></div>"
        self.assertEqual(html, expected)

    def test_empty_markdown(self):
        md = ""
        html = markdown_to_html_node(md).to_html()
        expected = "<div></div>"
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
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff</code></pre></div>"
        )
        self.assertEqual(html, expected)

    def test_heading_h1(self):
        md = "# Big heading"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><h1>Big heading</h1></div>"
        self.assertEqual(html, expected)

    def test_heading_h6(self):
        md = "###### Six deep"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><h6>Six deep</h6></div>"
        self.assertEqual(html, expected)

    def test_blockquote(self):
        md = "> first line\n> second line"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><blockquote>first line\nsecond line</blockquote></div>"
        self.assertEqual(html, expected)

    def test_unordered_list(self):
        md = "- alpha\n- beta\n- gamma"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div><ul><li>alpha</li><li>beta</li><li>gamma</li></ul></div>"
        )
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = "1. one\n2. two\n3. three"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>"
        )
        self.assertEqual(html, expected)

    def test_link_inline(self):
        md = "Click [here](https://example.com) please"
        html = markdown_to_html_node(md).to_html()
        expected = (
            '<div><p>Click <a href="https://example.com">here</a> please</p></div>'
        )
        self.assertEqual(html, expected)

    def test_image_inline(self):
        md = "See ![alt text](img.png) yes"
        html = markdown_to_html_node(md).to_html()
        expected = (
            '<div><p>See <img src="img.png" alt="alt text"></img> yes</p></div>'
        )
        self.assertEqual(html, expected)

    def test_mixed_blocks(self):
        md = "# Title\n\nSome _para_.\n\n- a\n- b"
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div><h1>Title</h1><p>Some <i>para</i>.</p>"
            "<ul><li>a</li><li>b</li></ul></div>"
        )
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
